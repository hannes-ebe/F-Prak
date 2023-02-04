program runge_kutta
    implicit none
    !declare precision
    integer, parameter :: ikind=selected_real_kind(p=20)
    ! declare variables
    real(kind=ikind), dimension(2d3) :: Q, I, Tl
    real(kind=ikind) :: dt,t,Q0, I0
    integer :: ci, steps
    !setup start varibles
    steps = SIZE(Q)-1
    dt=0.001
    open(10,file="start.txt")
    read(10,*)  Q0,I0
    Q(1) = Q0
    I(1) = I0
    Tl(1) = 0
    !iterate over time and solve runge kutta
    do ci = 1,steps
        t=dt*ci
        Tl(ci+1)=t
        call runge_kutta_step(t,dt,Q(ci),I(ci),Q(ci+1),I(ci+1))
    end do
    !Save results
    open(20,file="result_time.txt")
    write(20,*) Tl
    open(30,file="result_Q.txt")
    write(30,*) Q
    open(40,file="result_I.txt")
    write(40,*) I
    print *, "test"
end program runge_kutta

subroutine runge_kutta_step(t,dt,Q,I,Q_new,I_new)
    integer, parameter :: ikind=selected_real_kind(p=20)
    real(kind=ikind) :: Q,I,Q_new,I_new,Qk1,Qk2,Qk3,Qk4,Ik1,Ik2,Ik3,Ik4
    real(kind=ikind) :: t,dt
    !calculate Qks
    Qk1=fQ(t,Q,I)
    Qk2=fQ(t+ dt/2,Q+dt/2*Qk1,I+dt/2*Qk1)
    Qk3=fQ(t+ dt/2,Q+dt/2*Qk2,I+dt/2*Qk2)
    Qk4=fQ(t+ dt,Q+dt*Qk3,I+dt*Qk3)
    !calculate Iks
    Ik1=fI(t,Q,I)
    Ik2=fI(t+ dt/2,Q+dt/2*Ik1,I+dt/2*Ik1)
    Ik3=fI(t+ dt/2,Q+dt/2*Ik2,I+dt/2*Ik2)
    Ik4=fI(t+ dt,Q+dt*Ik3,I+dt*Ik3)
    !set new values
    Q_new=Q+(Qk1+2*Qk2+2*Qk3+Qk4)*dt*1/6
    I_new=I+(Ik1+2*Ik2+2*Ik3+Ik4)*dt*1/6
    end subroutine

function fQ(x,q,i)
    integer, parameter :: ikind=selected_real_kind(p=20)
    real(kind=ikind) :: x,q,i
    fQ=x
   end function
function fI(x,q,i)
    integer, parameter :: ikind=selected_real_kind(p=20)
    real(kind=ikind) :: x,q,i
    fI=2*x
   end function
