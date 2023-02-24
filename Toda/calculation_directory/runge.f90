MODULE toda
    CONTAINS
    function fQ(x,q,i,phi)
        integer, parameter :: ikind=selected_real_kind(p=20)
        real(kind=ikind) :: x,q,i,phi
        fQ=i
       end function fQ
    function fI(x,q,i,phi,U_pp,L,R,U_S,C0)
        integer, parameter :: ikind=selected_real_kind(p=20)
        real(kind=ikind) :: x,q,i,phi
        real(kind=ikind) :: U_pp,L,R,U_S,C0
        fI=-U_S/L*(EXP(q/(C0*U_S))-1)-R/L*i+U_pp/(2*L)*SIN(phi)
        !fI=-EXP(q)+1-0.2*i+5*SIN(phi)!-q/(C0*L)
       end function
    function fphi(x,q,i,phi,omega)
        integer, parameter :: ikind=selected_real_kind(p=20)
        real(kind=ikind) :: x,q,i,phi
        real(kind=ikind) :: omega
        fphi=omega
       end function
END MODULE toda

MODULE lorenz
    CONTAINS
    function fQ(x,q,i,phi)
    integer, parameter :: ikind=selected_real_kind(p=20)
    real(kind=ikind) :: x,q,i,phi
    fQ=10*(i-q)
   end function
function fI(x,q,i,phi,U_pp,L,R,U_S,C0)
    integer, parameter :: ikind=selected_real_kind(p=20)
    real(kind=ikind) :: x,q,i,phi
    real(kind=ikind) :: U_pp,L,R,U_S,C0
    fI=q*(28-phi)-i
   end function
function fphi(x,q,i,phi,omega)
    integer, parameter :: ikind=selected_real_kind(p=20)
    real(kind=ikind) :: x,q,i,phi
    real(kind=ikind) :: omega
    fphi=q*i-8/3*phi
   end function
END MODULE lorenz

MODULE LC
    CONTAINS
    function fQ(x,q,i,phi)
        integer, parameter :: ikind=selected_real_kind(p=15)
        real(kind=ikind) :: x,q,i,phi
        fQ=i
       end function fQ
    function fI(x,q,i,phi,U_pp,L,R,U_S,C0)
        integer, parameter :: ikind=selected_real_kind(p=15)
        real(kind=ikind) :: x,q,i,phi
        real(kind=ikind) :: U_pp,L,R,U_S,C0
        fI=-q/(C0*L)-R/L*i+U_pp/(2*L)*SIN(phi)
       end function
    function fphi(x,q,i,phi,omega)
        integer, parameter :: ikind=selected_real_kind(p=15)
        real(kind=ikind) :: x,q,i,phi
        real(kind=ikind) :: omega
        fphi=omega
    end function
END MODULE LC

program runge_kutta
    implicit none
    !declare precision
    integer, parameter :: ikind=selected_real_kind(p=20)
    ! declare variables
    real(kind=ikind), dimension(2d4) :: Q, I, phi, Tl
    real(kind=ikind), dimension(1d3) :: Q_temp, I_temp, phi_temp, Tl_temp
    real(kind=ikind) :: dt,t,Q0, I0
    real(kind=ikind) :: U_pp,L,R,U_S,C0,omega
    integer :: ci, ci_safe,steps,steps_to_safe
    !setup start varibles
    open(10,file="input/start.txt")
    read(10,*)  Q0,I0
    open(60,file="input/schwingkreis.txt")
    read(60,*)  U_pp,L,R,U_S,C0,omega
    open(70,file="input/simu.txt")
    read(70,*)  dt
    steps = SIZE(Q)-1
    steps_to_safe=SIZE(Q_temp)-1
    Q(1) = Q0
    I(1) = I0
    phi(1) = 0
    Tl(1) = 0
    !iterate over time and solve runge kutta
    print *,"start calculation"
    do ci = 1,steps
        Q_temp(1)=Q(ci)
        I_temp(1)=I(ci)
        phi_temp(1)=phi(ci)
        do ci_safe = 1,steps_to_safe
            t=dt*ci
            Tl(ci+1)=t
            call runge_kutta_step(t,dt,Q_temp(ci_safe),I_temp(ci_safe),phi_temp(ci_safe),Q_temp(ci_safe+1),I_temp(ci_safe+1),phi_temp(ci_safe+1),U_pp,L,R,U_S,C0,omega)
        end do
        Q(ci+1)=Q_temp(steps_to_safe)
        I(ci+1)=I_temp(steps_to_safe)
        phi(ci+1)=phi_temp(steps_to_safe)
    end do
    print *,"save data"
    !Save results
    open(20,file="output/result_time.txt")
    write(20,*) Tl
    open(30,file="output/result_Q.txt")
    write(30,*) Q
    open(40,file="output/result_I.txt")
    write(40,*) I
    open(50,file="output/result_phi.txt")
    write(50,*) phi
end program runge_kutta

subroutine runge_kutta_step(t,dt,Q,I,phi,Q_new,I_new,phi_new,U_pp,L,R,U_S,C0,omega)
    use toda
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

