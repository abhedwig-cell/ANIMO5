program test_kt01_runtime
  use iso_fortran_env, only: int64, real64
  use mod_animo_time_coordinate
  use mod_animo_runtime_contracts
  use mod_animo_kernel_transactions
  use mod_animo_committed_persistence
  use mod_animo_worker_context
  use mod_animo_interval_runtime
  implicit none
  integer :: f
  f=0
  call run_tests(f)
  if(f/=0) then; write(*,'(A,I0)') 'KT01 FORTRAN TEST FAILURES: ',f; error stop 1; endif
  write(*,'(A)') 'KT01 FORTRAN TESTS 01-23 AND 26-29: PASS'
contains
  subroutine a(x,n,f); logical,intent(in)::x; character(*),intent(in)::n; integer,intent(inout)::f
    if(x) then; write(*,'(A)') 'PASS '//trim(n); else; write(*,'(A)') 'FAIL '//trim(n); f=f+1; endif
  end subroutine
  subroutine mt(day,n,d,t,ok); integer(int64),intent(in)::day,n,d; type(TimeCoordinate),intent(out)::t; logical,intent(out)::ok
    call make_time_coordinate('ANIMO_CIVIL_DAY_V1',day,n,d,t,ok)
  end subroutine
  subroutine init(s,day,v); type(AcceptedState),intent(out)::s; integer(int64),intent(in)::day,v; logical::ok
    s=AcceptedState(); s%lineage_id='LINEAGE-A'; s%generation=7; call mt(day,0_int64,1_int64,s%accepted_time,ok); if(.not.ok) error stop 'fixture'; s%synthetic_storage=v; call clear_journal(s%committed_journal)
  end subroutine
  subroutine mr(s,t,d,r,complete,admit,ok)
    type(AcceptedState),intent(in)::s; type(TimeCoordinate),intent(in)::t; integer(int64),intent(in)::d
    type(TrialResult),intent(out)::r; logical,intent(in)::complete,admit; logical,intent(out)::ok
    type(TrialState)::tr; integer(int64)::v; logical::e
    r=TrialResult(); call begin_trial(s,t,tr,ok); if(.not.ok)return
    if(.not.checked_add_storage(tr%synthetic_storage,d,v))then; ok=.false.; return; endif
    tr%synthetic_storage=v; call append_transfer_event(tr%trial_journal,'SYNTHETIC_Q','OUT','CV',d,e); if(.not.e)then; ok=.false.; return; endif
    r%candidate=tr; r%n_assessments=1; r%assessments(1)%quantity_id='SYNTHETIC_Q'; r%assessments(1)%control_volume_id='CV'; r%assessments(1)%complete=complete; r%assessments(1)%admissible=admit; r%provenance_id='TEST'; ok=.true.
  end subroutine
  subroutine run_tests(f)
    integer,intent(inout)::f; type(AcceptedState)::s,b,rst; type(TimeCoordinate)::t,u,v; type(TrialResult)::r
    type(SyntheticAttemptPlan)::p2(2),p1(1); type(RuntimeTrace)::tr; type(AcceptedCheckpoint)::cp; type(WorkerContext)::w
    logical::ok,success,eq,ok2; character(80)::why; integer::ord; integer(int64)::g,bita,bitb; real(real64)::ra,rb

    call init(s,10_int64,100_int64); b=s; call mt(11_int64,0_int64,1_int64,t,ok); call mr(s,t,9_int64,r,.true.,.false.,ok); call reject_trial(r); call a(s%synthetic_storage==b%synthetic_storage.and.s%generation==b%generation.and.s%committed_journal%count==0,'01 reject preserves accepted',f)
    call init(s,20_int64,50_int64); call mt(21_int64,0_int64,1_int64,t,ok); p2=SyntheticAttemptPlan(); p2(1)%endpoint_time=t; p2(1)%storage_delta=1; p2(1)%conservation_admissible=.false.; p2(1)%retry_permitted_after_reject=.true.; p2(2)%endpoint_time=t; p2(2)%storage_delta=2; call run_synthetic_interval(s,t,p2,2,tr,success,why); call time_equal(tr%origin_time(1),tr%origin_time(2),eq,ok); call a(success.and.eq.and.tr%origin_generation(1)==tr%origin_generation(2),'02 retry same origin',f)
    call init(s,30_int64,10_int64); call mt(31_int64,0_int64,1_int64,t,ok); call mr(s,t,5_int64,r,.true.,.true.,ok); call commit_trial(s,r,ok,why); call a(ok.and.s%synthetic_storage==15.and.s%committed_journal%count==1,'03 atomic commit',f)
    call init(s,40_int64,10_int64); g=s%generation; call mt(41_int64,0_int64,1_int64,t,ok); call mr(s,t,1_int64,r,.true.,.true.,ok); call commit_trial(s,r,ok,why); call a(ok.and.s%generation==g+1,'04 generation once',f)
    call init(s,50_int64,10_int64); call mt(51_int64,0_int64,1_int64,t,ok); call mr(s,t,1_int64,r,.true.,.true.,ok); r%candidate%origin_generation=r%candidate%origin_generation-1; b=s; call commit_trial(s,r,ok,why); call a(.not.ok.and.trim(why)=='STALE_ORIGIN_GENERATION'.and.s%generation==b%generation,'05 stale revision rejects',f)
    call init(s,60_int64,10_int64); call mt(61_int64,0_int64,1_int64,t,ok); call mr(s,t,1_int64,r,.true.,.true.,ok); r%candidate%origin_lineage_id='OTHER'; call commit_trial(s,r,ok,why); call a(.not.ok.and.trim(why)=='LINEAGE_MISMATCH','06 lineage mismatch rejects',f)
    call init(s,70_int64,10_int64); call mt(71_int64,0_int64,1_int64,t,ok); call mr(s,t,1_int64,r,.true.,.true.,ok); call mt(69_int64,0_int64,1_int64,u,ok); r%candidate%origin_time=u; call commit_trial(s,r,ok,why); call a(.not.ok.and.trim(why)=='ORIGIN_TIME_MISMATCH','07 wrong origin time rejects',f)
    call init(s,80_int64,10_int64); call mt(81_int64,0_int64,1_int64,t,ok); call mr(s,t,3_int64,r,.true.,.false.,ok); call commit_trial(s,r,ok,why); call a(.not.ok.and.r%candidate%trial_journal%count==1.and.s%committed_journal%count==0,'08 rejected journal uncommitted',f)
    call init(s,90_int64,10_int64); b=s; call initialize_worker_context(w,'W',ok); call prepare_worker_attempt(w,'A','1',ok); w%scratch_value=999; w%attempt_diagnostic_counter=123; call a(s%synthetic_storage==b%synthetic_storage.and.s%generation==b%generation,'09 scratch diagnostics nonphysical',f)
    call init(s,100_int64,10_int64); call mt(101_int64,0_int64,1_int64,t,ok); call mr(s,t,100_int64,r,.true.,.false.,ok); call make_accepted_checkpoint(s,'CP1','L1','C1','F1',cp,ok); call a(ok.and.cp%synthetic_storage==10.and.cp%committed_journal%count==0,'10 checkpoint accepted only',f)
    call init(s,110_int64,22_int64); call make_accepted_checkpoint(s,'CP1','L1','C1','F1',cp,ok); call restore_accepted_checkpoint(cp,'CP1','L1','C1','F1',rst,ok,why); call time_equal(s%accepted_time,rst%accepted_time,eq,ok2); call a(ok.and.ok2.and.eq.and.rst%generation==s%generation.and.rst%synthetic_storage==s%synthetic_storage,'11 restore identity',f)
    call init(s,120_int64,22_int64); call make_accepted_checkpoint(s,'CP1','L1','C1','F1',cp,ok); call restore_accepted_checkpoint(cp,'CP2','L1','C1','F1',rst,ok,why); ok2=(.not.ok.and.trim(why)=='CHECKPOINT_SCHEMA_MISMATCH'); call restore_accepted_checkpoint(cp,'CP1','L2','C1','F1',rst,ok,why); call a(ok2.and..not.ok.and.trim(why)=='STATE_LAYOUT_MISMATCH','12 incompatible checkpoint rejects',f)
    call mt(130_int64,1_int64,3_int64,t,ok); call mt(130_int64,2_int64,6_int64,u,ok); call time_equal(t,u,eq,ok); call a(ok.and.eq,'13 exact time equality',f)
    call mt(140_int64,6_int64,4_int64,t,ok); call a(ok.and.t%day_index==141.and.t%subday_numerator==1.and.t%subday_denominator==2,'14 rational normalization',f)
    block; character(256)::txt; call mt(150_int64,7_int64,11_int64,t,ok); call serialize_time_coordinate(t,txt,ok); call deserialize_time_coordinate(trim(txt),u,ok); call time_equal(t,u,eq,ok2); call a(ok.and.ok2.and.eq.and.trim(txt)=='ANIMO_CIVIL_DAY_V1|150|7|11','15 exact time serialization',f); end block
    call mt(1000_int64,1_int64,18014398509481984_int64,t,ok); call mt(1000_int64,2_int64,18014398509481984_int64,u,ok); call time_compare(t,u,ord,ok); ra=real(t%day_index,real64)+real(t%subday_numerator,real64)/real(t%subday_denominator,real64); rb=real(u%day_index,real64)+real(u%subday_numerator,real64)/real(u%subday_denominator,real64); bita=transfer(ra,bita); bitb=transfer(rb,bitb); call a(ok.and.ord<0.and.bita==bitb,'16 rationals distinct despite REAL collapse',f)
    call mt(170_int64,0_int64,0_int64,t,ok); call mt(huge(0_int64),0_int64,1_int64,u,ok2); if(ok2)call time_add_fraction(u,1_int64,1_int64,v,ok2); call a(.not.ok.and..not.ok2,'17 invalid overflow time fails',f)
    call init(s,180_int64,10_int64); b=s; call mt(180_int64,1_int64,2_int64,u,ok); call mt(181_int64,0_int64,1_int64,t,ok); p1=SyntheticAttemptPlan(); p1(1)%endpoint_time=u; call run_synthetic_interval(s,t,p1,2,tr,success,why); call a(.not.success.and.trim(why)=='INCOMPLETE_INTERVAL_COMPLETION'.and.s%generation==b%generation,'18 exact target required',f)
    call init(s,190_int64,10_int64); call mt(191_int64,0_int64,1_int64,t,ok); p1=SyntheticAttemptPlan(); p1(1)%endpoint_time=s%accepted_time; p1(1)%conservation_admissible=.false.; p1(1)%retry_permitted_after_reject=.true.; call run_synthetic_interval(s,t,p1,1,tr,success,why); call a(.not.success.and.trim(why)=='NO_OR_BACKWARD_PROGRESS','19 no-progress retry fails',f)
    call initialize_worker_context(w,'W',ok); call prepare_worker_attempt(w,'A','1',ok); w%scratch_value=77; w%attempt_diagnostic_counter=9; call prepare_worker_attempt(w,'B','1',ok); call a(ok.and.trim(w%logical_model_id)=='B'.and.w%scratch_value==0.and.w%attempt_diagnostic_counter==0,'20 worker reuse isolated',f)
    call init(s,210_int64,10_int64); call mt(211_int64,0_int64,1_int64,t,ok); call mr(s,t,1_int64,r,.true.,.true.,ok); r%n_assessments=2; r%assessments(2)%quantity_id='Q2'; r%assessments(2)%control_volume_id='CV2'; r%assessments(2)%complete=.true.; r%assessments(2)%admissible=.true.; call commit_trial(s,r,ok,why); call a(ok.and.s%generation==8,'21 multiple conserved quantities',f)
    call init(s,220_int64,10_int64); call mt(221_int64,0_int64,1_int64,t,ok); call mr(s,t,1_int64,r,.false.,.true.,ok); call commit_trial(s,r,ok,why); call a(.not.ok.and.trim(why)=='ACCEPTANCE_REJECTED_OR_INCOMPLETE','22 incomplete conservation rejects',f)
    call init(s,230_int64,10_int64); call mt(231_int64,0_int64,1_int64,t,ok); p1=SyntheticAttemptPlan(); p1(1)%endpoint_time=t; p1(1)%storage_delta=5; p1(1)%transfer_amount=5; call run_synthetic_interval(s,t,p1,1,tr,success,why); call a(success.and.s%committed_journal%count==1.and.s%committed_journal%events(1)%amount==5,'23 no balancing event',f)
    call init(s,260_int64,10_int64); b=s; call mt(261_int64,0_int64,1_int64,t,ok); p1=SyntheticAttemptPlan(); p1(1)%endpoint_time=t; p1(1)%storage_delta=1; p1(1)%conservation_admissible=.false.; call run_synthetic_interval(s,t,p1,1,tr,success,why); call a(.not.success.and.trim(why)=='FAILED_ACCEPTANCE_AND_RETRY_POLICY'.and.s%generation==b%generation,'26 failed retry policy fails',f)
    call init(s,270_int64,10_int64); b=s; call mt(270_int64,1_int64,2_int64,u,ok); call mt(271_int64,0_int64,1_int64,t,ok); p2=SyntheticAttemptPlan(); p2(1)%endpoint_time=u; p2(2)%endpoint_time=t; call run_synthetic_interval(s,t,p2,1,tr,success,why); call a(.not.success.and.trim(why)=='ATTEMPT_BUDGET_EXHAUSTED'.and.s%generation==b%generation,'27 attempt exhaustion no publication',f)
    call init(s,280_int64,10_int64); call mt(281_int64,0_int64,1_int64,t,ok); call mt(282_int64,0_int64,1_int64,u,ok); p1=SyntheticAttemptPlan(); p1(1)%endpoint_time=u; call run_synthetic_interval(s,t,p1,1,tr,success,why); call a(.not.success.and.trim(why)=='ENDPOINT_BEYOND_REQUESTED_TARGET','28 beyond target fails',f)
    call init(s,290_int64,huge(0_int64)); call mt(291_int64,0_int64,1_int64,t,ok); p1=SyntheticAttemptPlan(); p1(1)%endpoint_time=t; p1(1)%storage_delta=1; call run_synthetic_interval(s,t,p1,1,tr,success,why); call a(.not.success.and.trim(why)=='SYNTHETIC_STATE_ARITHMETIC_UNREPRESENTABLE','29 unrepresentable state arithmetic fails',f)
  end subroutine
end program
