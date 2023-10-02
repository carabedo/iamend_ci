""" Modulo con las funciones del theodolidus """
import numpy
import scipy.integrate
import scipy.special
import scipy
from iamend_ci.aux import *

def zo(f,bo,lmax):
    """ Calculo de impedancia en aire (3.34) Zo para una bobina al aire"""
    mu0=4*3.14*1e-7
    r1=bo[0]
    r2=bo[1]
    dh=bo[2]
    N=bo[3]
    w=2*numpy.pi*f
    aint=(mu0*2*w*numpy.pi*N**2)/(((r2-r1)*dh)**2)
    return aint*cquad(lambda k:(k*dh + numpy.exp(-k*dh) - 1)*(ji(k,r1,r2)/k**3)**2,0,lmax)

def l0(bo,lmax):
    mu0=4*3.14*1e-7
    r1=bo[0]
    r2=bo[1]
    dh=bo[2]
    N=bo[3]
    aint=(mu0*2*numpy.pi*N**2)/(((r2-r1)*dh)**2)
    return aint*cquad(lambda k:(k*dh + numpy.exp(-k*dh) - 1)*(ji(k,r1,r2)/k**3)**2,0,lmax)


def dzHF(f,bo,sigma,mur,lmax):
    """ Calculo de impedancia en aire (3.52) im(dz) para una placa de espesor infinito"""
    dzhf=list()
    mu0=4*3.14*1e-7
    r1=bo[0]
    r2=bo[1]
    dh=bo[2]
    N=bo[3]
    z1=bo[4]
    l0=bo[5]
    aint=(1j*numpy.pi*(2*numpy.pi*f)*mu0*N**2)/(((r2-r1)*dh)**2)
    for i in range(0,len(f)):
        dzhf.append(cquad(lambda k: sig(k,sigma,f[i],mur)*(ji(k,r1,r2)*expz(k,z1,z1+dh))**2,0,lmax))
    return aint*dzhf




def dzD(f,bo,sigma,d,mur,lmax):
    """ Calculo de impedancia en aire (3.50) im(dz) para una placa de espesor 'd' """
    dzD=list()
    mu0=4*3.14*1e-7
    r1=bo[0]
    r2=bo[1]
    dh=bo[2]
    N=bo[3]
    z1=bo[4]
    l0=bo[5]
    aint=(1j*numpy.pi*(2*numpy.pi*f)*mu0*N**2)/(((r2-r1)*dh)**2)
    
    for i in range(0,len(f)):
        dzD.append(cquad(lambda k: sig2(k,sigma,f[i],d,mur)*(ji(k,r1,r2)*expz(k,z1,z1+dh))**2,0,lmax))
        
    return aint*numpy.array(dzD)




def dz2capas(f,bo,sigma1,sigma2,d,mur1,mur2,lmax):
    """ Calculo de impedancia im(dz) para dos layers 

    capa superior capa 1:
        - conductor ferromagnetico 1 de espesor d
    capa inferior capa 2:
        - conductor ferromagnetico 2 de espesor inf
        
    """

    dzD=list()
    mu0=4*3.14*1e-7
    r1=bo[0]
    r2=bo[1]
    dh=bo[2]
    N=bo[3]
    z1=bo[4]
    l0=bo[5]
    aint=(1j*numpy.pi*(2*numpy.pi*f)*mu0*N**2)/(((r2-r1)*dh)**2)
    for i in range(0,len(f)):
        dzD.append(cquad(lambda k: sig3(k,sigma1,sigma2,f[i],d,mur1,mur2)*(ji(k,r1,r2)*expz(k,z1,z1+dh))**2,0,lmax))
    return aint*numpy.array(dzD)


def jhf(r,z,I,f,bo,sigma,mur,lmax=1000):
    """ Calculo de densidad corriente sobre una placa semi-infinita """

    mu0=4*numpy.pi*1e-7
    r1=bo[0]
    r2=bo[1]
    dh=bo[2]
    N=bo[3]
    z1=bo[4]
    l0=bo[5]
    i0=N*I/((r2-r1)*dh)
    aint=1j*2*numpy.pi*f*sigma*mu0*i0
    inte=cquad(lambda k: scipy.special.j1(k*r)*ji(k,r1,r2)*expz(k,z1,z1+dh)*sigj(k,sigma,f,mur,z),0,lmax)
    
    return(aint*inte)



## Pancake

mu0=4*3.14*1e-7

def spiral_l0(coil):
    N=coil['N']
    a1=coil['a1']
    a2=coil['a2']
    h1=coil['h1']
    aint=(numpy.pi*mu0*(N**2))/((a2-a1)**2)
    lim=1e4
    int_uv=scipy.integrate.quad(lambda u: (u**-4)*I(u,a1,a2)**2,
                                        0, lim)
    return aint*int_uv[0]

def I(u,r1,r2):
    """ funcion auxiliar"""
    return     scipy.integrate.quad(lambda x: x*scipy.special.jv(1,x) ,u*r1,u*r2)[0]


def alfa1(u,f,sigma,mur):
  return numpy.sqrt(u + 1j*2*numpy.pi*f*sigma*mur*mu0 )

def sig(u,f,sigma,mur):
    up=mur*u-alfa1(u,f,sigma,mur)
    down=mur*u+alfa1(u,f,sigma,mur)
    return up/down

def spiral_dzhf(f,coil,muestra):
    N=coil['N']
    a1=coil['a1']
    a2=coil['a2']
    h1=coil['h1']
    w=2*numpy.pi*f
    sigma=muestra['sigma']
    mur=muestra['mur']

    aint=(1j*w*numpy.pi*mu0*(N**2))/((a2-a1)**2)
    lim=1e4

    re_int_uv=scipy.integrate.quad(lambda u: numpy.real((numpy.exp(-2*u*h1))*(u**-4)*sig(u,f,sigma,mur)*I(u,a1,a2)**2),
                                        0, lim)[0]
    im_int_uv=scipy.integrate.quad(lambda u: numpy.imag((numpy.exp(-2*u*h1))*(u**-4)*sig(u,f,sigma,mur)*I(u,a1,a2)**2),
                                        0, lim)[0]
    
    return aint*(re_int_uv + 1j*im_int_uv)