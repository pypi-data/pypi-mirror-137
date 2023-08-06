"""
module for GNSS processing
"""

from copy import deepcopy
from enum import IntEnum
from math import floor, sin, cos, sqrt, asin, atan2, fabs
import numpy as np

gpst0 = [1980, 1, 6, 0, 0, 0]


class rCST():
    """ class for constants """
    CLIGHT = 299792458.0
    MU_GPS = 3.9860050E14
    MU_GAL = 3.986004418E14
    GME = 3.986004415E+14
    GMS = 1.327124E+20
    GMM = 4.902801E+12
    OMGE = 7.2921151467E-5
    OMGE_GAL = 7.2921151467E-5
    RE_WGS84 = 6378137.0
    FE_WGS84 = (1.0/298.257223563)
    AU = 149597870691.0
    D2R = 0.017453292519943295
    AS2R = D2R/3600.0
    DAY_SEC = 86400.0
    CENTURY_SEC = DAY_SEC*36525.0


class uGNSS(IntEnum):
    """ class for GNSS constants """
    GPS = 0
    SBS = 1
    GAL = 2
    BDS = 3
    QZS = 5
    GLO = 6
    IRN = 7
    GNSSMAX = 8
    GPSMAX = 32
    GALMAX = 36
    QZSMAX = 10
    BDSMAX = 63
    GLOMAX = 24
    SBSMAX = 24
    IRNMAX = 10
#    BDSMAX = 0
#    GLOMAX = 0
#    SBSMAX = 0
#    IRNMAX = 0
    NONE = -1
    MAXSAT = GPSMAX+GLOMAX+GALMAX+BDSMAX+QZSMAX+SBSMAX+IRNMAX


class uSIG(IntEnum):
    """ class for GNSS signals """
    GPS_L1CA = 0
    GPS_L2W = 2
    GPS_L2CL = 3
    GPS_L2CM = 4
    GPS_L5Q = 6
    SBS_L1CA = 0
    GAL_E1C = 0
    GAL_E1B = 1
    GAL_E5BI = 5
    GAL_E5BQ = 6
    BDS_B1ID1 = 0
    BDS_B1ID2 = 1
    BDS_B2ID1 = 2
    BDS_B2ID2 = 3
    QZS_L1CA = 0
    QZS_L1S = 1
    QZS_L2CM = 4
    QZS_L2CL = 5
    GLO_L1OF = 0
    GLO_L2OF = 2
    NONE = -1
    SIGMAX = 8


class rSIG(IntEnum):
    """ class to define signals """
    NONE = 0
    L1C = 1
    L1X = 2
    L1W = 3
    L2L = 4
    L2X = 5
    L2W = 6
    L5Q = 7
    L5X = 8
    L7Q = 9
    L7X = 10
    SIGMAX = 16


class gtime_t():
    """ class to define the time """

    def __init__(self, time=0, sec=0.0):
        self.time = time
        self.sec = sec


class Obs():
    """ class to define the observation """

    def __init__(self):
        self.nm = 0
        self.t = gtime_t()
        self.P = []
        self.L = []
        self.S = []
        self.lli = []
        self.data = []
        self.sat = []


class Eph():
    """ class to define ephemeris """
    sat = 0
    iode = 0
    iodc = 0
    af0 = 0.0
    af1 = 0.0
    af2 = 0.0
    toc = 0
    toe = 0
    tot = 0
    week = 0
    crs = 0.0
    crc = 0.0
    cus = 0.0
    cus = 0.0
    cis = 0.0
    cic = 0.0
    e = 0.0
    i0 = 0.0
    A = 0.0
    deln = 0.0
    M0 = 0.0
    OMG0 = 0.0
    OMGd = 0.0
    omg = 0.0
    idot = 0.0
    tgd = 0.0
    tgd_b = 0.0
    sva = 0
    health = 0
    fit = 0
    toes = 0

    def __init__(self, sat=0):
        self.sat = sat


class Nav():
    """ class to define the navigation message """

    def __init__(self):
        self.eph = []
        self.ion = np.array([
            [0.1118E-07, -0.7451E-08, -0.5961E-07, 0.1192E-06],
            [0.1167E+06, -0.2294E+06, -0.1311E+06, 0.1049E+07]])
        self.elmin = np.deg2rad(15.0)
        self.tidecorr = False
        self.nf = 2
        self.excl_sat = []
        self.freq = [1.57542e9, 1.22760e9, 1.17645e9, 1.20714e9]
        self.rb = [0, 0, 0]  # base station position in ECEF [m]
        self.smode = 0  # position mode 0:NONE,1:std,2:DGPS,4:fix,5:float
        self.gnss_t = [uGNSS.GPS, uGNSS.GAL, uGNSS.QZS]
        # self.gnss_t = [uGNSS.GPS]
        self.loglevel = 1
        self.cnr_min = 35
        self.maxout = 5  # maximum outage [epoch]

        # antenna type:  JAVAD RINGANT SCIT
        self.ant_pcv = [[+0.00, -0.38, -1.46, -3.06, -4.94, -6.81, -8.45,
                         -9.66, -10.31, -10.35, -9.77, -8.62, -6.97, -4.85,
                         -2.22, 1.11, 5.45, 11.03, 17.84],
                        [+0.00, -0.16, -0.60, -1.26, -2.06, -2.91, -3.77,
                         -4.57, -5.21, -5.54, -5.43, -4.81, -3.69, -2.21,
                         -0.46, 1.58, 4.16, 7.70, 12.53],
                        [+0.00, -0.16, -0.60, -1.26, -2.06, -2.91, -3.77,
                         -4.57, -5.21, -5.54, -5.43, -4.81, -3.69, -2.21,
                         -0.46, 1.58, 4.16, 7.70, 12.53]]
        self.ant_pco = [+85.44, +115.05, +115.05]

        # antenna type: TRM59800.80     NONE [mm] 0:5:90 [deg]
        self.ant_pcv_b = [[+0.00, -0.22, -0.86, -1.87, -3.17, -4.62, -6.03,
                           -7.21, -7.98, -8.26, -8.02, -7.32, -6.20, -4.65,
                           -2.54, +0.37, +4.34, +9.45, +15.42],
                          [+0.00, -0.14, -0.53, -1.13, -1.89, -2.74, -3.62,
                           -4.43, -5.07, -5.40, -5.32, -4.79, -3.84, -2.56,
                           -1.02, +0.84, +3.24, +6.51, +10.84],
                          [+0.00, -0.14, -0.53, -1.13, -1.89, -2.74, -3.62,
                           -4.43, -5.07, -5.40, -5.32, -4.79, -3.84, -2.56,
                           -1.02, +0.84, +3.24, +6.51, +10.84]]
        self.ant_pco_b = [+89.51, +117.13, +117.13]

        # SSR correction placeholder
        self.dorb = np.zeros(uGNSS.MAXSAT)
        self.dclk = np.zeros(uGNSS.MAXSAT)
        self.dsis = np.zeros(uGNSS.MAXSAT)
        self.sis = np.zeros(uGNSS.MAXSAT)

        # satellite observation status
        self.fix = np.zeros((uGNSS.MAXSAT, self.nf), dtype=int)
        self.outc = np.zeros((uGNSS.MAXSAT, self.nf), dtype=int)
        self.vsat = np.zeros((uGNSS.MAXSAT, self.nf), dtype=int)
        self.lock = np.zeros((uGNSS.MAXSAT, self.nf), dtype=int)
        self.slip = np.zeros((uGNSS.MAXSAT, self.nf), dtype=int)

        self.tt = 0
        self.t = gtime_t()


def leaps(tgps):
    """ return leap seconds (TBD) """
    return -18.0


def epoch2time(ep):
    """ calculate time from epoch """
    doy = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
    time = gtime_t()
    year = int(ep[0])
    mon = int(ep[1])
    day = int(ep[2])

    if year < 1970 or year > 2099 or mon < 1 or mon > 12:
        return time
    days = (year-1970)*365+(year-1969)//4+doy[mon-1]+day-2
    if year % 4 == 0 and mon >= 3:
        days += 1
    sec = int(ep[5])
    time.time = days*86400+int(ep[3])*3600+int(ep[4])*60+sec
    time.sec = ep[5]-sec
    return time


def gpst2utc(tgps, leaps_=-18):
    """ calculate UTC-time from gps-time """
    tutc = timeadd(tgps, leaps_)
    return tutc


def timeadd(t: gtime_t, sec: float):
    """ return time added with sec """
    tr = deepcopy(t)
    tr.sec += sec
    tt = floor(tr.sec)
    tr.time += int(tt)
    tr.sec -= tt
    return tr


def timediff(t1: gtime_t, t2: gtime_t):
    """ return time difference """
    dt = t1.time-t2.time
    dt += t1.sec-t2.sec
    return dt


def gpst2time(week, tow):
    """ convert to time from gps-time """
    t = epoch2time(gpst0)
    if tow < -1e9 or tow > 1e9:
        tow = 0.0
    t.time += 86400*7*week+int(tow)
    t.sec = tow-int(tow)
    return t


def time2gpst(t: gtime_t):
    """ convert to gps-time from time """
    t0 = epoch2time(gpst0)
    sec = t.time-t0.time
    week = int(sec/(86400*7))
    tow = sec-week*86400*7+t.sec
    return week, tow


def time2epoch(t):
    """ convert time to epoch """
    mday = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 31, 28, 31, 30, 31,
            30, 31, 31, 30, 31, 30, 31, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31,
            30, 31, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    days = int(t.time/86400)
    sec = int(t.time-days*86400)
    day = days % 1461
    for mon in range(48):
        if day >= mday[mon]:
            day -= mday[mon]
        else:
            break
    ep = [0, 0, 0, 0, 0, 0]
    ep[0] = 1970+days//1461*4+mon//12
    ep[1] = mon % 12+1
    ep[2] = day+1
    ep[3] = sec//3600
    ep[4] = sec % 3600//60
    ep[5] = sec % 60+t.sec
    return ep


def time2doy(t):
    """ convert time to epoch """
    ep = time2epoch(t)
    ep[1] = ep[2] = 1.0
    ep[3] = ep[4] = ep[5] = 0.0
    return timediff(t, epoch2time(ep))/86400+1


def prn2sat(sys, prn):
    """ convert sys+prn to sat """
    if sys == uGNSS.GPS:
        sat = prn
    elif sys == uGNSS.GLO:
        sat = prn+uGNSS.GPSMAX
    elif sys == uGNSS.GAL:
        sat = prn+uGNSS.GPSMAX+uGNSS.GLOMAX
    elif sys == uGNSS.BDS:
        sat = prn+uGNSS.GPSMAX+uGNSS.GLOMAX+uGNSS.GALMAX
    elif sys == uGNSS.QZS:
        sat = prn-192+uGNSS.GPSMAX+uGNSS.GLOMAX+uGNSS.GALMAX+uGNSS.BDSMAX
    else:
        sat = 0
    return sat


def sat2prn(sat):
    """ convert sat to sys+prn """
    if sat > uGNSS.GPSMAX+uGNSS.GLOMAX+uGNSS.GALMAX+uGNSS.BDSMAX:
        prn = sat-(uGNSS.GPSMAX+uGNSS.GLOMAX+uGNSS.GALMAX+uGNSS.BDSMAX)+192
        sys = uGNSS.QZS
    elif sat > uGNSS.GPSMAX+uGNSS.GLOMAX+uGNSS.GALMAX:
        prn = sat-(uGNSS.GPSMAX+uGNSS.GLOMAX+uGNSS.GALMAX)
        sys = uGNSS.BDS
    elif sat > uGNSS.GPSMAX+uGNSS.GLOMAX:
        prn = sat-(uGNSS.GPSMAX+uGNSS.GLOMAX)
        sys = uGNSS.GAL
    elif sat > uGNSS.GPSMAX:
        prn = sat-uGNSS.GPSMAX
        sys = uGNSS.GLO
    else:
        prn = sat
        sys = uGNSS.GPS
    return (sys, prn)


def sat2id(sat):
    """ convert satellite number to id """
    sys, prn = sat2prn(sat)
    gnss_tbl = {uGNSS.GPS: 'G', uGNSS.GAL: 'E', uGNSS.BDS: 'C',
                uGNSS.QZS: 'J', uGNSS.GLO: 'R'}
    if sys not in gnss_tbl:
        return -1
    if sys == uGNSS.QZS:
        prn -= 192
    elif sys == uGNSS.SBS:
        prn -= 100
    return '%s%02d' % (gnss_tbl[sys], prn)


def id2sat(id_):
    """ convert id to satellite number """
    # gnss_tbl={'G':uGNSS.GPS,'S':uGNSS.SBS,'E':uGNSS.GAL,'C':uGNSS.BDS,
    #           'I':uGNSS.IRN,'J':uGNSS.QZS,'R':uGNSS.GLO}
    gnss_tbl = {'G': uGNSS.GPS, 'E': uGNSS.GAL, 'C': uGNSS.BDS,
                'J': uGNSS.QZS, 'R': uGNSS.GLO}
    if id_[0] not in gnss_tbl:
        return -1
    sys = gnss_tbl[id_[0]]
    prn = int(id_[1:3])
    if sys == uGNSS.QZS:
        prn += 192
    elif sys == uGNSS.SBS:
        prn += 100
    sat = prn2sat(sys, prn)
    return sat


def vnorm(r):
    """ calculate norm of a vector """
    return r/np.linalg.norm(r)


def geodist(rs, rr):
    """ calculate geometric distance """
    e = rs-rr
    r = np.linalg.norm(e)
    e = e/r
    r += rCST.OMGE*(rs[0]*rr[1]-rs[1]*rr[0])/rCST.CLIGHT
    return r, e


def kfupdate(x, P, H, v, R):
    """ Kalman filter measurement update """
    # select subset of states and covariance
    ix = []
    for i in range(len(x)):
        if P[i, i] > 0.0:
            ix.append(i)
    x_ = x[ix]
    P_ = P[ix, :][:, ix]
    # measurement update
    H_ = H[:, ix]
    PHt = P_@H_.T
    S = H_@PHt+R
    K = PHt@np.linalg.inv(S)
    x_ += K@v
    P_ -= K@H_@P_
    # restore states and covariance
    x[ix] = x_
    sP = P[ix, :]
    sP[:, ix] = P_
    P[ix, :] = sP
    return x, P, S


def dops_h(H):
    """ calculate DOP from H """
    Qinv = np.linalg.inv(np.dot(H.T, H))
    dop = np.diag(Qinv)
    hdop = dop[0]+dop[1]  # TBD
    vdop = dop[2]  # TBD
    pdop = hdop+vdop
    gdop = pdop+dop[3]
    dop = np.array([gdop, pdop, hdop, vdop])
    return dop


def dops(az, el, elmin=0):
    """ calculate DOP from az/el """
    nm = az.shape[0]
    H = np.zeros((nm, 4))
    n = 0
    for i in range(nm):
        if el[i] < elmin:
            continue
        cel = cos(el[i])
        sel = sin(el[i])
        H[n, 0] = cel*sin(az[i])
        H[n, 1] = cel*cos(az[i])
        H[n, 2] = sel
        H[n, 3] = 1
        n += 1
    if n < 4:
        return None
    Qinv = np.linalg.inv(np.dot(H.T, H))
    dop = np.diag(Qinv)
    hdop = dop[0]+dop[1]  # TBD
    vdop = dop[2]  # TBD
    pdop = hdop+vdop
    gdop = pdop+dop[3]
    dop = np.array([gdop, pdop, hdop, vdop])
    return dop


def xyz2enu(pos):
    """ return ECEF to ENU conversion matrix from LLH """
    sp = sin(pos[0])
    cp = cos(pos[0])
    sl = sin(pos[1])
    cl = cos(pos[1])
    E = np.array([[-sl, cl, 0],
                  [-sp*cl, -sp*sl, cp],
                  [cp*cl, cp*sl, sp]])
    return E


def ecef2pos(r):
    """  ECEF to LLH position conversion """
    e2 = rCST.FE_WGS84*(2-rCST.FE_WGS84)
    r2 = r[0]**2+r[1]**2
    v = rCST.RE_WGS84
    z = r[2]
    cnt = 0
    while cnt < 1000:
        zk = z
        sp = z/np.sqrt(r2+z**2)
        v = rCST.RE_WGS84/np.sqrt(1-e2*sp**2)
        z = r[2]+v*e2*sp
        if np.fabs(z-zk) < 1e-4:
            break
        cnt += 1
    pos = np.array([np.arctan(z/np.sqrt(r2)),
                    np.arctan2(r[1], r[0]),
                    np.sqrt(r2+z**2)-v])
    return pos


def pos2ecef(pos, isdeg: bool = False):
    """ LLH (rad/deg) to ECEF position conversion  """
    if isdeg:
        pos[0] *= np.pi/180.0
        pos[1] *= np.pi/180.0
    s_p = sin(pos[0])
    c_p = cos(pos[0])
    s_l = sin(pos[1])
    c_l = cos(pos[1])
    e2 = rCST.FE_WGS84*(2.0-rCST.FE_WGS84)
    v = rCST.RE_WGS84/sqrt(1.0-e2*s_p**2)
    r = np.array([(v+pos[2])*c_p*c_l,
                  (v+pos[2])*c_p*s_l,
                  (v*(1.0-e2)+pos[2])*s_p])
    return r


def ecef2enu(pos, r):
    """ releative ECEF to ENU conversion """
    E = xyz2enu(pos)
    e = E@r
    return e


def deg2dms(deg):
    """ convert from deg to dms """
    if deg < 0.0:
        sign = -1
    else:
        sign = 1
    a = fabs(deg)
    dms = np.zeros(3)
    dms[0] = floor(a)
    a = (a-dms[0])*60.0
    dms[1] = floor(a)
    a = (a-dms[1])*60.0
    dms[2] = a
    dms[0] *= sign
    return dms


def satazel(pos, e):
    """ calculate az/el from LOS vector in ECEF (e) """
    enu = ecef2enu(pos, e)
    az = atan2(enu[0], enu[1])
    el = asin(enu[2])
    return az, el


def ionmodel(t, pos, az, el, ion=None):
    """ klobuchar model of ionosphere delay estimation """
    psi = 0.0137/(el/np.pi+0.11)-0.022
    phi = pos[0]/np.pi+psi*cos(az)
    phi = np.max((-0.416, np.min((0.416, phi))))
    lam = pos[1]/np.pi+psi*sin(az)/cos(phi*np.pi)
    phi += 0.064*cos((lam-1.617)*np.pi)
    _, tow = time2gpst(t)
    tt = 43200.0*lam+tow  # local time
    tt -= np.floor(tt/86400)*86400
    f = 1.0+16.0*np.power(0.53-el/np.pi, 3.0)  # slant factor

    h = [1, phi, phi**2, phi**3]
    amp = np.dot(h, ion[0, :])
    per = np.dot(h, ion[1, :])
    amp = max(amp, 0)
    per = max(per, 72000.0)
    x = 2.0*np.pi*(tt-50400.0)/per
    if np.abs(x) < 1.57:
        v = 5e-9+amp*(1.0+x*x*(-0.5+x*x/24.0))
    else:
        v = 5e-9
    diono = rCST.CLIGHT*f*v
    return diono


def interpc(coef, lat):
    """ linear interpolation (lat step=15) """
    i = int(lat/15.0)
    if i < 1:
        return coef[:, 0]
    if i > 4:
        return coef[:, 4]
    d = lat/15.0-i
    return coef[:, i-1]*(1.0-d)+coef[:, i]*d


def antmodel(nav, el=0, nf=2, rtype=1):
    """ antenna pco/pcv """
    sE = sin(el)
    za = 90-np.rad2deg(el)
    za_t = np.arange(0, 90.1, 5)
    dant = np.zeros(nf)
    if rtype == 1:  # for rover
        pcv_t = nav.ant_pcv
        pco_t = nav.ant_pco
    else:  # for base
        pcv_t = nav.ant_pcv_b
        pco_t = nav.ant_pco_b
    for f in range(nf):
        pcv = np.interp(za, za_t, pcv_t[f])
        pco = -pco_t[f]*sE
        dant[f] = (pco+pcv)*1e-3
    return dant


def mapf(el, a, b, c):
    """ simple tropospheric mapping function """
    sinel = np.sin(el)
    return (1.0+a/(1.0+b/(1.0+c)))/(sinel+(a/(sinel+b/(sinel+c))))


def tropmapf(t, pos, el):
    """ tropospheric mapping function by Neil (NMF) """
    if pos[2] < -1e3 or pos[2] > 20e3 or el <= 0.0:
        return 0.0, 0.0
    coef = np.array([
        [1.2769934E-3, 1.2683230E-3, 1.2465397E-3, 1.2196049E-3, 1.2045996E-3],
        [2.9153695E-3, 2.9152299E-3, 2.9288445E-3, 2.9022565E-3, 2.9024912E-3],
        [62.610505E-3, 62.837393E-3, 63.721774E-3, 63.824265E-3, 64.258455E-3],
        [0.0000000E-0, 1.2709626E-5, 2.6523662E-5, 3.4000452E-5, 4.1202191E-5],
        [0.0000000E-0, 2.1414979E-5, 3.0160779E-5, 7.2562722E-5, 11.723375E-5],
        [0.0000000E-0, 9.0128400E-5, 4.3497037E-5, 84.795348E-5, 170.37206E-5],
        [5.8021897E-4, 5.6794847E-4, 5.8118019E-4, 5.9727542E-4, 6.1641693E-4],
        [1.4275268E-3, 1.5138625E-3, 1.4572752E-3, 1.5007428E-3, 1.7599082E-3],
        [4.3472961E-2, 4.6729510E-2, 4.3908931E-2, 4.4626982E-2, 5.4736038E-2],
    ])
    aht = [2.53E-5, 5.49E-3, 1.14E-3]
    lat = np.rad2deg(pos[0])
    hgt = pos[2]
    y = (time2doy(t)-28.0)/365.25
    if lat < 0.0:
        y += 0.5
    cosy = np.cos(2.0*np.pi*y)
    lat = np.abs(lat)
    c = interpc(coef, lat)
    ah = c[0:3]-c[3:6]*cosy
    aw = c[6:9]
    dm = (1.0/np.sin(el)-mapf(el, aht[0], aht[1], aht[2]))*hgt*1e-3
    mapfh = mapf(el, ah[0], ah[1], ah[2])+dm
    mapfw = mapf(el, aw[0], aw[1], aw[2])
    return mapfh, mapfw


def tropmodel(t, pos, el=np.pi/2, humi=0.7):
    """ saastamonien tropospheric delay model """
    hgt = pos[2]
    # standard atmosphere
    pres = 1013.25*np.power(1-2.2557e-5*hgt, 5.2568)
    temp = 15.0-6.5e-3*hgt+273.16
    e = 6.108*humi*np.exp((17.15*temp-4684.0)/(temp-38.45))
    # saastamoinen
    z = np.pi/2.0-el
    trop_hs = 0.0022768*pres/(1.0-0.00266*np.cos(2*pos[0])-0.00028e-3*hgt)
    trop_wet = 0.002277*(1255.0/temp+0.05)*e
    return trop_hs, trop_wet, z
