program test_kt12_tcd042_client
  use iso_fortran_env, only: int64, real64
  use mod_transient_time, only: TimeCoordinate, make_time_coordinate
  use mod_transient_contracts, only: transient_payload_t
  use mod_transient_transactions, only: accepted_store_t, accepted_store_generation, &
    accepted_store_time, snapshot_accepted_payload
  use mod_transient_interval_runtime, only: attempt_request_t, runtime_trace_t, run_interval
  use mod_animo_tcd042_upper_boundary_client, only: &
    tcd042_resolved_hydrology_t, tcd042_top_state_t, tcd042_upper_boundary_client_t, &
    TCD042_RESOLVED_HYDROLOGY_SCHEMA, TCD042_BRANCH_B1_EXACT_ZERO, &
    TCD042_BRANCH_E1_NQ03, initialize_tcd042_store, configure_tcd042_client, &
    tcd042_last_diagnostics
  implicit none

  call test_exact_zero_commit()
  call test_finite_positive_nq03_commit()
  call test_outside_scope_reject_preserves_store()
  call test_resolved_hydrology_guards()
  print *, 'PASS_KT12_TCD042_TRANSACTION_RUNTIME_CLIENT'

contains

  logical function exact_binary_zero(value)
    real(real64), intent(in) :: value
    integer(int64) :: bits
    bits = transfer(value, bits)
    exact_binary_zero = iand(bits, int(z'7FFFFFFFFFFFFFFF', int64)) == 0_int64
  end function exact_binary_zero

  subroutine assert_true(value, message)
    logical, intent(in) :: value
    character(len=*), intent(in) :: message
    if (.not. value) then
      print *, 'ASSERTION FAILED: ', trim(message)
      error stop 1
    end if
  end subroutine assert_true

  subroutine make_day(day, value)
    integer(int64), intent(in) :: day
    type(TimeCoordinate), intent(out) :: value
    logical :: ok
    call make_time_coordinate('ANIMO_TEST_CALENDAR', day, 0_int64, 1_int64, value, ok)
    call assert_true(ok, 'make time')
  end subroutine make_day

  subroutine one_request(endpoint, requests)
    type(TimeCoordinate), intent(in) :: endpoint
    type(attempt_request_t), intent(out) :: requests(1)
    requests(1)%endpoint_time = endpoint
    requests(1)%retry_permitted_after_reject = .false.
  end subroutine one_request

  subroutine extract_concentration(store, concentration)
    type(accepted_store_t), intent(in) :: store
    real(real64), intent(out) :: concentration
    class(transient_payload_t), allocatable :: copy
    logical :: ok
    call snapshot_accepted_payload(store, copy, ok)
    call assert_true(ok, 'snapshot payload')
    select type (typed => copy)
    type is (tcd042_top_state_t)
      concentration = typed%concentration
    class default
      call assert_true(.false., 'wrong payload type')
    end select
  end subroutine extract_concentration

  function base_hydrology(flib_top) result(h)
    real(real64), intent(in) :: flib_top
    type(tcd042_resolved_hydrology_t) :: h
    h%schema_id = TCD042_RESOLVED_HYDROLOGY_SCHEMA
    h%flpn = 0
    h%flib_top = flib_top
    h%rurv = 0.0_real64
  end function base_hydrology

  subroutine test_exact_zero_commit()
    type(TimeCoordinate) :: t0, t1, actual_time
    type(accepted_store_t) :: store
    type(tcd042_upper_boundary_client_t) :: client
    type(tcd042_resolved_hydrology_t) :: hydro
    type(attempt_request_t) :: requests(1)
    type(runtime_trace_t) :: trace
    logical :: ok, success, valid
    character(len=48) :: reason
    real(real64) :: c, avg, flux, p
    integer :: branch_id

    call make_day(0_int64, t0)
    call make_day(1_int64, t1)
    call initialize_tcd042_store(store, 'KT12_B1', t0, 1.0_real64, ok)
    call assert_true(ok, 'initialize exact-zero store')

    hydro = base_hydrology(0.0_real64)
    call configure_tcd042_client(client, hydro, 0.5_real64, 0.25_real64, ok)
    call assert_true(ok, 'configure exact-zero client')
    call one_request(t1, requests)

    call run_interval(store, client, t1, requests, 1, trace, success, reason)
    call assert_true(success, 'exact-zero interval success')
    call assert_true(trim(reason) == 'INTERVAL_COMMITTED', 'exact-zero runtime reason')
    call assert_true(accepted_store_generation(store) == 1_int64, 'generation advances once')
    call extract_concentration(store, c)
    call assert_true(transfer(c, 0_int64) == transfer(1.5_real64, 0_int64), 'B1 exact end concentration')

    call tcd042_last_diagnostics(client, avg, flux, p, branch_id, valid)
    call assert_true(valid, 'B1 diagnostics valid')
    call assert_true(branch_id == TCD042_BRANCH_B1_EXACT_ZERO, 'B1 branch')
    call assert_true(transfer(avg, 0_int64) == transfer(1.25_real64, 0_int64), 'B1 exact average concentration')
    call assert_true(exact_binary_zero(flux) .and. exact_binary_zero(p), 'B1 zero flux and P')
    call accepted_store_time(store, actual_time, ok)
    call assert_true(ok .and. actual_time%day_index == 1_int64, 'B1 accepted time')
  end subroutine test_exact_zero_commit

  subroutine test_finite_positive_nq03_commit()
    type(TimeCoordinate) :: t0, t1
    type(accepted_store_t) :: store
    type(tcd042_upper_boundary_client_t) :: client
    type(tcd042_resolved_hydrology_t) :: hydro
    type(attempt_request_t) :: requests(1)
    type(runtime_trace_t) :: trace
    logical :: ok, success, valid
    character(len=48) :: reason
    real(real64) :: c, avg, flux, p
    integer :: branch_id

    call make_day(10_int64, t0)
    call make_day(11_int64, t1)
    call initialize_tcd042_store(store, 'KT12_E1', t0, 1.0_real64, ok)
    call assert_true(ok, 'initialize E1 store')

    hydro = base_hydrology(2.0_real64**(-30))
    call configure_tcd042_client(client, hydro, 1.0_real64, 0.25_real64, ok)
    call assert_true(ok, 'configure E1 client')
    call one_request(t1, requests)

    call run_interval(store, client, t1, requests, 1, trace, success, reason)
    call assert_true(success, 'E1 interval success')
    call extract_concentration(store, c)
    call assert_true(transfer(c, 0_int64) == int(z'3ff3ffffffb80000', int64), 'E1 end concentration bit pattern')

    call tcd042_last_diagnostics(client, avg, flux, p, branch_id, valid)
    call assert_true(valid, 'E1 diagnostics valid')
    call assert_true(branch_id == TCD042_BRANCH_E1_NQ03, 'E1 branch')
    call assert_true(transfer(avg, 0_int64) == int(z'3ff1ffffffdd5555', int64), 'E1 average concentration bit pattern')
    call assert_true(transfer(flux, 0_int64) == int(z'3e10000000000000', int64), 'E1 flux bit pattern')
    call assert_true(transfer(p, 0_int64) == int(z'3e10000000000000', int64), 'E1 P bit pattern')
  end subroutine test_finite_positive_nq03_commit

  subroutine test_outside_scope_reject_preserves_store()
    type(TimeCoordinate) :: t0, t1, actual_time
    type(accepted_store_t) :: store
    type(tcd042_upper_boundary_client_t) :: client
    type(tcd042_resolved_hydrology_t) :: hydro
    type(attempt_request_t) :: requests(1)
    type(runtime_trace_t) :: trace
    logical :: ok, success, valid
    character(len=48) :: reason
    real(real64) :: c, avg, flux, p
    integer :: branch_id

    call make_day(20_int64, t0)
    call make_day(21_int64, t1)
    call initialize_tcd042_store(store, 'KT12_REJECT', t0, 2.0_real64, ok)
    call assert_true(ok, 'initialize reject store')

    hydro = base_hydrology(1.0e-8_real64)
    call configure_tcd042_client(client, hydro, 1.0_real64, 0.25_real64, ok)
    call assert_true(ok, 'configure out-of-scope client')
    call one_request(t1, requests)

    call run_interval(store, client, t1, requests, 1, trace, success, reason)
    call assert_true(.not. success, 'out-of-scope fails')
    call assert_true(trim(reason) == 'CLIENT_ATTEMPT_FAILED', 'runtime collapses client failure')
    call assert_true(accepted_store_generation(store) == 0_int64, 'rejected generation unchanged')
    call extract_concentration(store, c)
    call assert_true(transfer(c, 0_int64) == transfer(2.0_real64, 0_int64), 'rejected concentration unchanged')
    call accepted_store_time(store, actual_time, ok)
    call assert_true(ok .and. actual_time%day_index == 20_int64, 'rejected time unchanged')
    call tcd042_last_diagnostics(client, avg, flux, p, branch_id, valid)
    call assert_true(.not. valid, 'rejected diagnostics invalid')
  end subroutine test_outside_scope_reject_preserves_store

  subroutine test_resolved_hydrology_guards()
    type(tcd042_upper_boundary_client_t) :: client
    type(tcd042_resolved_hydrology_t) :: hydro
    logical :: ok

    hydro = base_hydrology(0.0_real64)
    hydro%flpn = 1
    call configure_tcd042_client(client, hydro, 0.02_real64, 0.0_real64, ok)
    call assert_true(.not. ok, 'ponded hydrology rejected')

    hydro = base_hydrology(0.0_real64)
    hydro%rurv = 1.0e-12_real64
    call configure_tcd042_client(client, hydro, 0.02_real64, 0.0_real64, ok)
    call assert_true(.not. ok, 'Flpn=0 nonzero Rurv rejected')

    hydro = base_hydrology(-1.0e-12_real64)
    call configure_tcd042_client(client, hydro, 0.02_real64, 0.0_real64, ok)
    call assert_true(.not. ok, 'negative Flib rejected')

    hydro = base_hydrology(0.0_real64)
    call configure_tcd042_client(client, hydro, 0.0_real64, 0.0_real64, ok)
    call assert_true(.not. ok, 'Hetop zero rejected')
  end subroutine test_resolved_hydrology_guards

end program test_kt12_tcd042_client
