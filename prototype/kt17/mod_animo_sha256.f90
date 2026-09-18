module mod_animo_sha256
  use iso_fortran_env, only: int64
  implicit none
  private

  integer(int64), parameter :: MASK32 = int(z'00000000FFFFFFFF',int64)
  integer(int64), parameter :: BYTE_MASK = int(z'00000000000000FF',int64)
  integer(int64), parameter :: K(0:63) = [ &
    int(z'428A2F98',int64), int(z'71374491',int64), int(z'B5C0FBCF',int64), int(z'E9B5DBA5',int64), &
    int(z'3956C25B',int64), int(z'59F111F1',int64), int(z'923F82A4',int64), int(z'AB1C5ED5',int64), &
    int(z'D807AA98',int64), int(z'12835B01',int64), int(z'243185BE',int64), int(z'550C7DC3',int64), &
    int(z'72BE5D74',int64), int(z'80DEB1FE',int64), int(z'9BDC06A7',int64), int(z'C19BF174',int64), &
    int(z'E49B69C1',int64), int(z'EFBE4786',int64), int(z'0FC19DC6',int64), int(z'240CA1CC',int64), &
    int(z'2DE92C6F',int64), int(z'4A7484AA',int64), int(z'5CB0A9DC',int64), int(z'76F988DA',int64), &
    int(z'983E5152',int64), int(z'A831C66D',int64), int(z'B00327C8',int64), int(z'BF597FC7',int64), &
    int(z'C6E00BF3',int64), int(z'D5A79147',int64), int(z'06CA6351',int64), int(z'14292967',int64), &
    int(z'27B70A85',int64), int(z'2E1B2138',int64), int(z'4D2C6DFC',int64), int(z'53380D13',int64), &
    int(z'650A7354',int64), int(z'766A0ABB',int64), int(z'81C2C92E',int64), int(z'92722C85',int64), &
    int(z'A2BFE8A1',int64), int(z'A81A664B',int64), int(z'C24B8B70',int64), int(z'C76C51A3',int64), &
    int(z'D192E819',int64), int(z'D6990624',int64), int(z'F40E3585',int64), int(z'106AA070',int64), &
    int(z'19A4C116',int64), int(z'1E376C08',int64), int(z'2748774C',int64), int(z'34B0BCB5',int64), &
    int(z'391C0CB3',int64), int(z'4ED8AA4A',int64), int(z'5B9CCA4F',int64), int(z'682E6FF3',int64), &
    int(z'748F82EE',int64), int(z'78A5636F',int64), int(z'84C87814',int64), int(z'8CC70208',int64), &
    int(z'90BEFFFA',int64), int(z'A4506CEB',int64), int(z'BEF9A3F7',int64), int(z'C67178F2',int64) ]

  public :: sha256_ascii

contains

  pure integer(int64) function u32(x) result(v)
    integer(int64), intent(in) :: x
    v = iand(x,MASK32)
  end function u32

  pure integer(int64) function rotr32(x,n) result(v)
    integer(int64), intent(in) :: x
    integer, intent(in) :: n
    integer(int64) :: y
    y = u32(x)
    v = u32(ior(shiftr(y,n),shiftl(y,32-n)))
  end function rotr32

  pure integer(int64) function big_sigma0(x) result(v)
    integer(int64), intent(in) :: x
    v = u32(ieor(ieor(rotr32(x,2),rotr32(x,13)),rotr32(x,22)))
  end function big_sigma0

  pure integer(int64) function big_sigma1(x) result(v)
    integer(int64), intent(in) :: x
    v = u32(ieor(ieor(rotr32(x,6),rotr32(x,11)),rotr32(x,25)))
  end function big_sigma1

  pure integer(int64) function small_sigma0(x) result(v)
    integer(int64), intent(in) :: x
    v = u32(ieor(ieor(rotr32(x,7),rotr32(x,18)),shiftr(u32(x),3)))
  end function small_sigma0

  pure integer(int64) function small_sigma1(x) result(v)
    integer(int64), intent(in) :: x
    v = u32(ieor(ieor(rotr32(x,17),rotr32(x,19)),shiftr(u32(x),10)))
  end function small_sigma1

  pure integer(int64) function choose32(x,y,z) result(v)
    integer(int64), intent(in) :: x,y,z
    v = u32(ieor(iand(u32(x),u32(y)),iand(not(u32(x)),u32(z))))
  end function choose32

  pure integer(int64) function majority32(x,y,z) result(v)
    integer(int64), intent(in) :: x,y,z
    v = u32(ieor(ieor(iand(u32(x),u32(y)),iand(u32(x),u32(z))), &
      iand(u32(y),u32(z))))
  end function majority32

  pure integer(int64) function virtual_byte(text,n,total,pos) result(v)
    character(len=*), intent(in) :: text
    integer(int64), intent(in) :: n,total,pos
    integer(int64) :: bit_length, shift_count

    if (pos < n) then
      v = int(iachar(text(int(pos)+1:int(pos)+1)),int64)
    else if (pos == n) then
      v = 128_int64
    else if (pos >= total-8_int64) then
      bit_length = n*8_int64
      shift_count = 8_int64*(total-1_int64-pos)
      v = iand(shiftr(bit_length,int(shift_count)),BYTE_MASK)
    else
      v = 0_int64
    end if
  end function virtual_byte

  pure subroutine lowercase_hex(value)
    character(len=*), intent(inout) :: value
    integer :: i,c
    do i=1,len(value)
      c=iachar(value(i:i))
      if(c>=iachar('A') .and. c<=iachar('F')) value(i:i)=achar(c+32)
    end do
  end subroutine lowercase_hex

  function sha256_ascii(text) result(hex)
    character(len=*), intent(in) :: text
    character(len=64) :: hex

    integer(int64) :: h(0:7),w(0:63)
    integer(int64) :: a,b,c,d,e,f,g,hh,t1,t2
    integer(int64) :: n,total,block_start,pos
    integer :: i,j

    n=int(len(text),int64)
    if(n > (huge(n)-9_int64)) then
      hex=''
      return
    end if
    total=((n+9_int64+63_int64)/64_int64)*64_int64

    h=[ &
      int(z'6A09E667',int64), int(z'BB67AE85',int64), &
      int(z'3C6EF372',int64), int(z'A54FF53A',int64), &
      int(z'510E527F',int64), int(z'9B05688C',int64), &
      int(z'1F83D9AB',int64), int(z'5BE0CD19',int64) ]

    block_start=0_int64
    do while(block_start < total)
      do i=0,15
        w(i)=0_int64
        do j=0,3
          pos=block_start+int(4*i+j,int64)
          w(i)=u32(ior(shiftl(w(i),8),virtual_byte(text,n,total,pos)))
        end do
      end do
      do i=16,63
        w(i)=u32(small_sigma1(w(i-2))+w(i-7)+small_sigma0(w(i-15))+w(i-16))
      end do

      a=h(0); b=h(1); c=h(2); d=h(3)
      e=h(4); f=h(5); g=h(6); hh=h(7)

      do i=0,63
        t1=u32(hh+big_sigma1(e)+choose32(e,f,g)+K(i)+w(i))
        t2=u32(big_sigma0(a)+majority32(a,b,c))
        hh=g
        g=f
        f=e
        e=u32(d+t1)
        d=c
        c=b
        b=a
        a=u32(t1+t2)
      end do

      h(0)=u32(h(0)+a)
      h(1)=u32(h(1)+b)
      h(2)=u32(h(2)+c)
      h(3)=u32(h(3)+d)
      h(4)=u32(h(4)+e)
      h(5)=u32(h(5)+f)
      h(6)=u32(h(6)+g)
      h(7)=u32(h(7)+hh)

      block_start=block_start+64_int64
    end do

    write(hex,'(8(Z8.8))') h
    call lowercase_hex(hex)
  end function sha256_ascii

end module mod_animo_sha256
