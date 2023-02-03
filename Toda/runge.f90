program runge_kutta
    implicit none
    ! This is a comment line; it is ignored by the compiler
    real, dimension(10d1) :: Q, I
    real :: dt,t
    integer :: ci, steps
    steps = SIZE(Q)-1
    dt=0.1
    Q(0) = 0
    I(0) = 0
    do ci = 0,steps
        t=dt*ci
        call runge_kutta_step(t,dt,Q(ci),I(ci),Q(ci+1),I(ci+1))
        print *, ci,t,Q(ci),Q(ci+1)
    end do
end program runge_kutta

subroutine runge_kutta_step(t,dt,Q,I,Q_new,I_new)
    real :: Q,I,Q_new,I_new,k1,k2,k3,k4
    real :: t,dt
    k1=f(t,Q)
    k2=f(t+ dt/2,Q+dt/2*k1)
    k3=f(t+ dt/2,Q+dt/2*k2)
    k4=f(t+ dt,Q+h*k3)
    Q_new=Q+(k1+2*k2+2*k3+k4)*dt*1/6
    end subroutine

function f(x,u)
    real :: x,u
    f=x
   end function

