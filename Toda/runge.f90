program runge_kutta
    implicit none
    ! This is a comment line; it is ignored by the compiler
    real, dimension(10d1) :: Q, I
    integer :: ci, steps
    steps = SIZE(Q)-1
    Q(0) = 1
    I(0) = 1
    do ci = 0,steps
        call runge_kutta_step(Q(ci),I(ci),Q(ci+1),I(ci+1))
        print *, ci,Q(ci),Q(ci+1),I(ci),I(ci+1)
    end do
end program runge_kutta

subroutine runge_kutta_step(Q,I,Q_new,I_new)
    real :: Q,I,Q_new,I_new
    Q_new = Q+1
    I_new = I+1
    end subroutine

