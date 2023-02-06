program runge_kutta
    implicit none
    !declare precision
    integer, parameter :: ikind=selected_real_kind(p=20)
    ! declare variables
    real(kind=ikind), dimension(1d5) :: Q, I, phi, Tl
    real(kind=ikind) :: dt,t,Q0, I0
    real(kind=ikind) :: U_pp,L,R,U_S,C0,omega
    integer :: ci, steps
    !setup start varibles
    open(10,file="input/start.txt")
    read(10,*)  Q0,I0
    open(60,file="input/schwingkreis.txt")
    read(60,*)  U_pp,L,R,U_S,C0,omega
    steps = SIZE(Q)-1
    dt=1d-8
    Q(1) = Q0
    I(1) = I0
    phi(1) = 0
    Tl(1) = 0
    !iterate over time and solve runge kutta
    do ci = 1,steps
        t=dt*ci
        Tl(ci+1)=t
        call runge_kutta_step(t,dt,Q(ci),I(ci),phi(ci),Q(ci+1),I(ci+1),phi(ci+1),U_pp,L,R,U_S,C0,omega)
    end do
    !Save results
    open(20,file="output/result_time.txt")
    write(20,*) Tl
    open(30,file="output/result_Q.txt")
    write(30,*) Q
    open(40,file="output/result_I.txt")
    write(40,*) I
    open(50,file="output/result_phi.txt")
    write(50,*) phi
    print *, "testa"
end program runge_kutta

subroutine runge_kutta_step(t,dt,Q,I,phi,Q_new,I_new,phi_new,U_pp,L,R,U_S,C0,omega)
    integer, parameter :: ikind=selected_real_kind(p=20)
    real(kind=ikind) :: Q,I,Q_new,I_new,phi,phi_new
    real(kind=ikind) :: Qk1,Qk2,Qk3,Qk4,Ik1,Ik2,Ik3,Ik4,pk1,pk2,pk3,pk4
    real(kind=ikind) :: t,dt
    real(kind=ikind) :: U_pp,L,R,U_S,C0,omega, PI
    !calculate Qks
    Qk1=fQ(t,Q,I,phi)
    pk1=fphi(t,Q,I,phi,omega)
    Ik1=fI(t,Q,I,phi,U_pp,L,R,U_S,C0)
    Qk2=fQ(t+dt/2,Q+dt/2*Qk1,I+dt/2*Ik1,phi+dt/2*pk1)
    Ik2=fI(t+dt/2,Q+dt/2*Qk1,I+dt/2*Ik1,phi+dt/2*pk1,U_pp,L,R,U_S,C0)
    pk2=fphi(t+dt/2,Q+dt/2*Qk1,I+dt/2*Ik1,phi+dt/2*pk1,omega)
    Qk3=fQ(t+dt/2,Q+dt/2*Qk2,I+dt/2*Ik2,phi+dt/2*pk2)
    Ik3=fI(t+dt/2,Q+dt/2*Qk2,I+dt/2*Ik2,phi+dt/2*pk2,U_pp,L,R,U_S,C0)
    pk3=fphi(t+dt/2,Q+dt/2*Qk2,I+dt/2*Ik2,phi+dt/2*pk2,omega)
    Qk4=fQ(t+dt,Q+dt*Qk3,I+dt*Ik3,phi+dt*pk3)
    Ik4=fI(t+dt,Q+dt*Qk3,I+dt*Ik3,phi+dt*pk3,U_pp,L,R,U_S,C0)
    pk4=fphi(t+dt,Q+dt*Qk3,I+dt*Ik3,phi+dt*pk3,omega)
    !set new values
    !print *,(Ik1+2*Ik2+2*Ik3+Ik4)*1/6
    Q_new=Q+(Qk1+2*Qk2+2*Qk3+Qk4)*dt*1/6
    I_new=I+(Ik1+2*Ik2+2*Ik3+Ik4)*dt*1/6
    phi_new=phi+(pk1+2*pk2+2*pk3+pk4)*dt*1/6
    end subroutine

function fQ(x,q,i,phi)
    integer, parameter :: ikind=selected_real_kind(p=20)
    real(kind=ikind) :: x,q,i,phi
    fQ=i
   end function
function fI(x,q,i,phi,U_pp,L,R,U_S,C0)
    integer, parameter :: ikind=selected_real_kind(p=20)
    real(kind=ikind) :: x,q,i,phi
    real(kind=ikind) :: U_pp,L,R,U_S,C0
    !print *,-q/(C0*L)-R/L*i+U_pp/L*SIN(phi)
    fI=-q/(C0*L)-R/L*i+U_pp/L*SIN(phi)
   end function
function fphi(x,q,i,phi,omega)
    integer, parameter :: ikind=selected_real_kind(p=20)
    real(kind=ikind) :: x,q,i,phi
    real(kind=ikind) :: omega
    fphi=omega
   end function
