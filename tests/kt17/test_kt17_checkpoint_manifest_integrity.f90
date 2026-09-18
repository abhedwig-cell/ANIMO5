program test_kt17_checkpoint_manifest_integrity
  use iso_fortran_env, only: int64, real64
  use mod_transient_time, only: TimeCoordinate, make_time_coordinate
  use mod_transient_contracts, only: transient_payload_t
  use mod_transient_transactions, only: accepted_store_t
  use mod_animo_sha256, only: sha256_ascii
  use mod_animo_static_boundary_year_binding, only: &
    boundary_year_cursor_t, initialize_boundary_year_cursor
  use mod_animo_detailed_hydrology_origin_state, only: &
    detailed_hydrology_origin_state_t, make_detailed_hydrology_origin_state
  use mod_animo_composite_accepted_continuation, only: &
    composite_accepted_continuation_t, initialize_composite_continuation
  use mod_animo_tcd042_upper_boundary_client, only: &
    tcd042_top_state_t, initialize_tcd042_store
  use mod_animo_atomic_composite_application, only: &
    kt15_static_hydrology_config_t, kt15_application_config_t, &
    kt15_application_state_t, make_kt15_application_config, &
    same_kt15_application_config, initialize_kt15_application_state, &
    kt15_application_generation, kt15_application_time, &
    snapshot_kt15_science_payload, snapshot_kt15_application_config
  use mod_animo_checkpoint_manifest_integrity, only: &
    kt17_checkpoint_envelope_t, encode_kt17_checkpoint_envelope, &
    verify_kt17_checkpoint_envelope, restore_kt17_checkpoint_envelope, &
    canonical_kt15_config_hash, canonical_kt16_checkpoint_hash, &
    KT17_SOURCE_ARCHIVE_SHA256, KT17_TESTBANK_SHA256, KT17_DOCUMENTATION_SHA256
  implicit none

  call test_sha256_standard_vectors()
  call test_encode_verify_restore()
  call test_payload_tamper_rejected()
  call test_manifest_identity_tamper_rejected()
  call test_expected_build_and_config_mismatch_rejected()
  print *, 'PASS_KT17_CHECKPOINT_MANIFEST_INTEGRITY_BUILD_IDENTITY'

contains

  subroutine assert_true(value,message)
    logical,intent(in)::value
    character(len=*),intent(in)::message
    if(.not.value)then
      print *,'ASSERTION FAILED: ',trim(message)
      error stop 1
    end if
  end subroutine assert_true

  subroutine make_day(index,value)
    integer(int64),intent(in)::index
    type(TimeCoordinate),intent(out)::value
    logical::ok
    call make_time_coordinate('ANIMO_PG_86400_NOLEAPSECONDS_V1',index,0_int64,1_int64,value,ok)
    call assert_true(ok,'make exact time')
  end subroutine make_day

  subroutine make_config(hash,load_channel,config)
    character(len=*),intent(in)::hash
    integer,intent(in)::load_channel
    type(kt15_application_config_t),intent(out)::config
    type(kt15_static_hydrology_config_t)::hydro
    logical::ok
    character(len=128)::reason

    hydro=kt15_static_hydrology_config_t()
    hydro%he_top=1.0_real64
    hydro%lefrrv=0.0_real64
    hydro%lefrso=0.0_real64
    call make_kt15_application_config('ANIMO_PG_86400_NOLEAPSECONDS_V1',0_int64,hydro, &
      hash,2000,load_channel,config,ok,reason)
    call assert_true(ok,'make immutable application config')
  end subroutine make_config

  subroutine initialize_application(lineage,config,state)
    character(len=*),intent(in)::lineage
    type(kt15_application_config_t),intent(in)::config
    type(kt15_application_state_t),intent(out)::state

    type(TimeCoordinate)::t0
    type(accepted_store_t)::store
    type(detailed_hydrology_origin_state_t)::origin
    type(boundary_year_cursor_t)::cursor
    type(composite_accepted_continuation_t)::continuation
    real(real64)::mofro(1)
    logical::ok
    character(len=128)::reason

    call make_day(730119_int64,t0)
    call initialize_tcd042_store(store,lineage,t0,1.25_real64,ok)
    call assert_true(ok,'initialize science store')

    mofro=[0.5_real64]
    call make_detailed_hydrology_origin_state(0.0_real64,0.0_real64,0.0_real64, &
      mofro,origin,ok,reason)
    call assert_true(ok,'make hydrology origin')
    call initialize_boundary_year_cursor(cursor)
    call initialize_composite_continuation(lineage,t0,origin,0.0_real64,cursor, &
      continuation,ok,reason)
    call assert_true(ok,'make composite continuation')
    call initialize_kt15_application_state(store,continuation,config,state,ok,reason)
    call assert_true(ok,'initialize accepted application')
  end subroutine initialize_application

  subroutine snapshot_concentration(state,value)
    type(kt15_application_state_t),intent(in)::state
    real(real64),intent(out)::value
    class(transient_payload_t),allocatable::copy
    logical::ok

    value=0.0_real64
    call snapshot_kt15_science_payload(state,copy,ok)
    call assert_true(ok,'snapshot science payload')
    select type(typed=>copy)
    type is(tcd042_top_state_t)
      value=typed%concentration
    class default
      call assert_true(.false.,'wrong science payload type')
    end select
  end subroutine snapshot_concentration

  subroutine test_sha256_standard_vectors()
    character(len=64)::h
    character(len=*),parameter::long_message = &
      'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq'

    h=sha256_ascii('')
    call assert_true(h=='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', &
      'SHA256 empty vector')
    h=sha256_ascii('abc')
    call assert_true(h=='ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad', &
      'SHA256 abc vector')
    h=sha256_ascii(long_message)
    call assert_true(h=='248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1', &
      'SHA256 long vector')
  end subroutine test_sha256_standard_vectors

  subroutine test_encode_verify_restore()
    character(len=*),parameter::build='1234567890abcdef1234567890abcdef12345678'
    character(len=*),parameter::boundary_hash = &
      '629a94972504c2865f8f0cbae9960e1354f6acd09e39ef663cc8f74375a7a169'
    type(kt15_application_config_t)::config,restored_config
    type(kt15_application_state_t)::state,restored
    type(kt17_checkpoint_envelope_t)::envelope
    type(TimeCoordinate)::t
    character(len=64)::config_hash,payload_hash
    character(len=128)::reason
    logical::ok
    real(real64)::c

    call make_config(boundary_hash,1,config)
    call initialize_application('KT17-VALID',config,state)

    call encode_kt17_checkpoint_envelope(state,build,envelope,ok,reason)
    call assert_true(ok,'encode KT17 envelope')
    call assert_true(envelope%source_archive_sha256==KT17_SOURCE_ARCHIVE_SHA256,'source evidence pin')
    call assert_true(envelope%testbank_sha256==KT17_TESTBANK_SHA256,'testbank evidence pin')
    call assert_true(envelope%documentation_sha256==KT17_DOCUMENTATION_SHA256,'documentation evidence pin')

    call canonical_kt15_config_hash(envelope%checkpoint%config,config_hash,ok,reason)
    call assert_true(ok .and. config_hash==envelope%application_config_sha256,'config hash recomputes')
    call canonical_kt16_checkpoint_hash(envelope%checkpoint,payload_hash,ok,reason)
    call assert_true(ok .and. payload_hash==envelope%checkpoint_payload_sha256,'payload hash recomputes')

    call verify_kt17_checkpoint_envelope(envelope,build,config,ok,reason)
    call assert_true(ok,'verify KT17 envelope')
    call restore_kt17_checkpoint_envelope(envelope,build,config,restored,ok,reason)
    call assert_true(ok,'restore verified KT17 envelope')
    call assert_true(kt15_application_generation(restored)==0_int64,'restored generation exact')
    call kt15_application_time(restored,t,ok)
    call assert_true(ok .and. t%day_index==730119_int64,'restored accepted time exact')
    call snapshot_concentration(restored,c)
    call assert_true(transfer(c,0_int64)==transfer(1.25_real64,0_int64),'restored science exact')
    call snapshot_kt15_application_config(restored,restored_config,ok)
    call assert_true(ok .and. same_kt15_application_config(config,restored_config), &
      'restored immutable config exact')
  end subroutine test_encode_verify_restore

  subroutine test_payload_tamper_rejected()
    character(len=*),parameter::build='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    character(len=*),parameter::boundary_hash = &
      '629a94972504c2865f8f0cbae9960e1354f6acd09e39ef663cc8f74375a7a169'
    type(kt15_application_config_t)::config
    type(kt15_application_state_t)::state
    type(kt17_checkpoint_envelope_t)::envelope,bad
    character(len=128)::reason
    logical::ok

    call make_config(boundary_hash,1,config)
    call initialize_application('KT17-TAMPER',config,state)
    call encode_kt17_checkpoint_envelope(state,build,envelope,ok,reason)
    call assert_true(ok,'encode tamper fixture')

    bad=envelope
    bad%checkpoint%tcd042_concentration=bad%checkpoint%tcd042_concentration+1.0_real64
    call verify_kt17_checkpoint_envelope(bad,build,config,ok,reason)
    call assert_true(.not.ok .and. trim(reason)=='KT17_CHECKPOINT_PAYLOAD_INTEGRITY_MISMATCH', &
      'payload tamper rejected by recomputed hash')

    bad=envelope
    bad%checkpoint_payload_sha256='bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'
    call verify_kt17_checkpoint_envelope(bad,build,config,ok,reason)
    call assert_true(.not.ok,'declared payload digest tamper rejected')

    bad=envelope
    bad%manifest_sha256='cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc'
    call verify_kt17_checkpoint_envelope(bad,build,config,ok,reason)
    call assert_true(.not.ok,'manifest digest tamper rejected')
  end subroutine test_payload_tamper_rejected

  subroutine test_manifest_identity_tamper_rejected()
    character(len=*),parameter::build='dddddddddddddddddddddddddddddddddddddddd'
    character(len=*),parameter::boundary_hash = &
      '629a94972504c2865f8f0cbae9960e1354f6acd09e39ef663cc8f74375a7a169'
    type(kt15_application_config_t)::config
    type(kt15_application_state_t)::state
    type(kt17_checkpoint_envelope_t)::envelope,bad
    character(len=128)::reason
    logical::ok

    call make_config(boundary_hash,1,config)
    call initialize_application('KT17-MANIFEST',config,state)
    call encode_kt17_checkpoint_envelope(state,build,envelope,ok,reason)
    call assert_true(ok,'encode identity fixture')

    bad=envelope
    bad%source_archive_sha256='eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
    call verify_kt17_checkpoint_envelope(bad,build,config,ok,reason)
    call assert_true(.not.ok .and. trim(reason)=='KT17_EVIDENCE_IDENTITY_MISMATCH', &
      'source evidence identity tamper rejected')

    bad=envelope
    bad%feature_set_id='OTHER'
    call verify_kt17_checkpoint_envelope(bad,build,config,ok,reason)
    call assert_true(.not.ok .and. trim(reason)=='KT17_FEATURE_SET_MISMATCH', &
      'feature set tamper rejected')
  end subroutine test_manifest_identity_tamper_rejected

  subroutine test_expected_build_and_config_mismatch_rejected()
    character(len=*),parameter::build='ffffffffffffffffffffffffffffffffffffffff'
    character(len=*),parameter::other_build='1111111111111111111111111111111111111111'
    character(len=*),parameter::boundary_hash = &
      '629a94972504c2865f8f0cbae9960e1354f6acd09e39ef663cc8f74375a7a169'
    type(kt15_application_config_t)::config,wrong
    type(kt15_application_state_t)::state
    type(kt17_checkpoint_envelope_t)::envelope
    character(len=128)::reason
    logical::ok

    call make_config(boundary_hash,1,config)
    call make_config(boundary_hash,2,wrong)
    call initialize_application('KT17-EXPECT',config,state)
    call encode_kt17_checkpoint_envelope(state,build,envelope,ok,reason)
    call assert_true(ok,'encode expectation fixture')

    call verify_kt17_checkpoint_envelope(envelope,other_build,config,ok,reason)
    call assert_true(.not.ok .and. trim(reason)=='KT17_EXPECTED_BUILD_ID_MISMATCH', &
      'expected build mismatch rejected')

    call verify_kt17_checkpoint_envelope(envelope,build,wrong,ok,reason)
    call assert_true(.not.ok .and. trim(reason)=='KT17_EXPECTED_CONFIG_MISMATCH', &
      'expected config mismatch rejected')
  end subroutine test_expected_build_and_config_mismatch_rejected

end program test_kt17_checkpoint_manifest_integrity
