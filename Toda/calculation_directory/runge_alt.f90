program runge_kutta
    implicit none
    !declare precision
    integer, parameter :: ikind=selected_real_kind(p=20)
    ! declare variables
    real(kind=ikind), dimension(1d4) :: Q, I, phi, Tl
    real(kind=ikind) :: dt,t,Q0, I0
    integer :: ci, steps
    !setup start varibles
    steps = SIZE(Q)-1
    dt=1d-6
    open(10,file="start.txt")
    read(10,*)  Q0,I0
    Q(1) = Q0
    I(1) = I0
    phi(1) = 0
    Tl(1) = 0
    !iterate over time and solve runge kutta
    do ci = 1,steps
        t=dt*ci
        Tl(ci+1)=t
        call runge_kutta_step(t,dt,Q(ci),I(ci),phi(ci),Q(ci+1),I(ci+1),phi(ci+1))
    end do
    !Save results
    open(20,file="result_time.txt")
    write(20,*) Tl
    open(30,file="result_Q.txt")
    write(30,*) Q
    open(40,file="result_I.txt")
    write(40,*) I
    open(50,file="result_phi.txt")
    write(50,*) phi
    print *, "test"
end program runge_kutta

subroutine runge_kutta_step(t,dt,Q,I,phi,Q_new,I_new,phi_new)
    integer, parameter :: ikind=selected_real_kind(p=20)
    real(kind=ikind) :: Q,I,Q_new,I_new,phi,phi_new
    real(kind=ikind) :: Qk1,Qk2,Qk3,Qk4,Ik1,Ik2,Ik3,Ik4,pk1,pk2,pk3,pk4
    real(kind=ikind) :: t,dt
    real(kind=ikind) :: U_pp,L,R,U_S,C0,omega, PI
    !open(50,file="schwingkreis.txt")
    !read(50,*)  U_pp,L,R,U_S,C0,omega
    U_pp=0.04
    L=65*1e-3
    R=1e3
    U_S=-0.3
    C0=100*1e-12
    PI=4.D0*DATAN(1.D0)
    omega=2*55*10d3*PI
    !calculate Qks
    Qk1=fQ(t,Q,I,phi)
    Qk2=fQ(t+ dt/2,Q+dt/2*Qk1,I+dt/2*Qk1,phi+dt/2*Qk1)
    Qk3=fQ(t+ dt/2,Q+dt/2*Qk2,I+dt/2*Qk2,phi+dt/2*Qk2)
    Qk4=fQ(t+ dt,Q+dt*Qk3,I+dt*Qk3,phi+dt*Qk3)
    !calculate Iks
    Ik1=fI(t,Q,I,phi,U_pp,L,R,U_S,C0)
    Ik2=fI(t+ dt/2,Q+dt/2*Ik1,I+dt/2*Ik1,phi+dt/2*Ik1,U_pp,L,R,U_S,C0)
    Ik3=fI(t+ dt/2,Q+dt/2*Ik2,I+dt/2*Ik2,phi+dt/2*Ik2,U_pp,L,R,U_S,C0)
    Ik4=fI(t+ dt,Q+dt*Ik3,I+dt*Ik3,phi+dt*Ik3,U_pp,L,R,U_S,C0)
    !print *,"ks",Ik1,Ik2,Ik3,Ik4,I+dt/2*Ik1
    !calculate phi ks
    pk1=fphi(t,Q,I,phi,omega)
    pk2=fphi(t+ dt/2,Q+dt/2*Ipk1,I+dt/2*pk1,phi+dt/2*pk1,omega)
    pk3=fphi(t+ dt/2,Q+dt/2*pk2,I+dt/2*pk2,phi+dt/2*pk2,omega)
    pk4=fphi(t+ dt,Q+dt*pk3,I+dt*pk3,phi+dt*pk3,omega)
    !set new values
    !print *,Qk1+2*Qk2+2*Qk3+Qk4
    Q_new=Q+(Qk1+2*Qk2+2*Qk3+Qk4)*dt*1/6
    I_new=I+(Ik1+2*Ik2+2*Ik3+Ik4)*dt*1/6
    phi_new=phi+(pk1+2*pk2+2*pk3+pk4)*dt*1/6
    !print *,(pk1+2*pk2+2*pk3+pk4)
    end subroutine

function fQ(x,q,i,phi)
    integer, parameter :: ikind=selected_real_kind(p=20)
    real(kind=ikind) :: x,q,i,phi
    fQ=i
   end function
function fI(x,q,i,phi,U_pp,L,R,U_S,C0)
    integer, parameter :: ikind=selected_real_kind(p=20)
    real(kind=ikind) :: x,q,i,phi,test
    real(kind=ikind) :: U_pp,L,R,U_S,C0
    !print *,i
    fI=U_pp/L*SIN(phi)-R/L*i-U_S/L*(EXP(q/(C0*U_S))-1)
   end function
function fphi(x,q,i,phi,omega)
    integer, parameter :: ikind=selected_real_kind(p=20)
    real(kind=ikind) :: x,q,i,phi
    real(kind=ikind) :: omega
    fphi=omega
   end function
