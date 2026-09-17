module mod_kt06_lwkm_interval_fixture
  use iso_fortran_env, only: real64
  implicit none
  private

  integer, parameter, public :: LWKM_LAYER_COUNT = 30
  integer, parameter, public :: LWKM_DRAINAGE_COUNT = 5
  real(real64), parameter, public :: LWKM_ENDPOINT_DAY = 10.0_real64
  real(real64), parameter, public :: LWKM_STEP_DAYS = 10.0_real64
  real(real64), parameter, public :: LWKM_SICT_END = 0.0_real64
  character(len=*), parameter, public :: LWKM_DYNAMIC_GROUP_SHA256 = &
    '2e5e8ff7c088ddd94f91aeb663ea10abdecfda0ac4cd418a8bf90be955389ec7'
end module mod_kt06_lwkm_interval_fixture
