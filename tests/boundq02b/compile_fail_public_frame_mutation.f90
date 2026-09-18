program compile_fail_boundq02b_public_mutation
  use mod_animo_immutable_static_boundary_frame, only: immutable_static_boundary_interval_frame_t
  implicit none
  type(immutable_static_boundary_interval_frame_t) :: frame

  ! This must not compile: scientific frame content is opaque outside its owner module.
  frame%selected_slot = 1
end program compile_fail_boundq02b_public_mutation
