program tcd034_post_do_probe
  implicit none
  integer :: ln, lnroot

  lnroot = 3
  do ln = 1, lnroot
     continue
  end do
  if (ln /= 4) error stop 11
  write(*,'(A,I0)') 'normal_post_do_ln=', ln

  ! Negative control: the deepest rooted compartment would require an
  ! explicit reset. The frozen TCD-034 source does not contain this reset.
  ln = lnroot
  if (ln /= 3) error stop 12
  write(*,'(A,I0)') 'explicit_reset_negative_control_ln=', ln
end program tcd034_post_do_probe
