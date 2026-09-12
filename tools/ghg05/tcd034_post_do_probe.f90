program tcd034_post_do_probe
  implicit none
  integer :: ln, lnroot

  lnroot = 3
  do ln = 1, lnroot
     continue
  end do
  if (ln /= 4) error stop 11
  write(*,'(A,I0)') 'positive_trip_post_do_ln=', ln

  ! Runtime root reconstruction can set Nuroup/LnRoot to zero.
  ! Under current standard Fortran semantics the zero-trip loop still
  ! establishes the control variable at its initial value, here 1.
  lnroot = 0
  do ln = 1, lnroot
     continue
  end do
  if (ln /= 1) error stop 12
  write(*,'(A,I0)') 'zero_trip_post_do_ln=', ln

  ! Negative control: selecting the deepest rooted compartment would require
  ! an explicit reset. The frozen TCD-034 path contains no such reset.
  lnroot = 3
  ln = lnroot
  if (ln /= 3) error stop 13
  write(*,'(A,I0)') 'explicit_reset_negative_control_ln=', ln
end program tcd034_post_do_probe
