def setup_e2v(PL=-6.0,Pswing=10.5,Sswing=9.5,RGswing=10.5,RD_PU=8):
    #==========================================================
    # function name : setup_e2v 
    # Authors : P.Antilogus & C.Juramy
    # Version : V4 , Oct 10 2024
    #      V4 : This version allows to estimate setup  "off main road"  for  // swing bellow 9V & // Low=-6 V
    #                                   
    # goal          : provide the various e2v voltages implied by a set of "free" parameters
    # input         : 4 "free" parameters that can be set independently the one from the others and that will
    #                  fix all the other e2v voltages 
    # 1)        PL  : Parallel Clock Low voltage 
    #                 default value : -6 V 
    #                 - Lower the value is better the serial CTE will be, also low value allow a more 
    #                   efficient holes uniformisation  / improve Rabbits ears - devisadiro effect
    #                 -  The lowest acceptable value , for safety raison ( avoid current in the bulk )  is -6V 
    #                 as this value already includes a huge  margins , it is a reasonnable default value. 
    # 2)        Pswing :  Parallel swing 
    #                  default value : 10.5 V
    #                 - higher the value is , better will be the full well and lower will be the BF effect
    #                 - the REB / power supply set 10.5 V as a reasonnable maximum ( even if e2v device have all
    #                    bin tested at 11V by e2v ... they implemented the complex 4 // phases configuration to 
    #                   allow a large usefull fullwell )
    #                 - Noise for fast-// clock rate - large swing has been observed in BOT - SLAC power supply
    #                    , the current cure is to limit the Pswing to 9.6 V ( hopefully a change in // clock sequence
    #                    could fix this as well , and will allow to increase  Pswing )
    #                 - large Pswing is bad for tearing ... the current limit for this reason is // swing = 9.3 V
    # 3)       Sswing   : Serial swing
    #                  default = 9.5 V
    #                  - A minimal value is 9 V
    #                  - For a conservative reason we use 9.3 V in the focal plane for years 
    #                  - e2v recommand 9.5 V and this value was used in all sensor qualification .
    # 4)       RGswing   : Reset Gate Swing
    #                  default Value   : 10.5 V
    #                  - What really matter for RG is the value of RG up which is not affected by the choice of
    #                    RGswing in this code.
    #                  - RGswing is only used to set RGlow, which has some freedom . In e2v setup RGswing is set 
    #                    to 12.5 V , but value as low as 10V should be fine , at the moment RG up is set correctly
    #                  - In the cold the REB can only deliver a swing up to 10.7 V 
    #
    #Initial seting ===========================================  
    #  channel potential : provided by e2v
    CHZ=11
    #  Reference BSS used in unipolar , and // upper and // lower used in this case 
    BSS_ref=-50
    Pup_ref=9.3
    Plow_ref=0.
    # minimal value that REB can deliver
    OG_min=-3.75
    # End initial seting =======================================
    # All The other voltages can be computed from above numbers :
    # Compute related voltages =================================
    # PU = Pswing+PL
    PU = Pswing+PL
    # RD , should be such than clamp by PU (=phi4) will work  :  
    # RD=PU+7 initial e2v setup , BNL default in unipolar test RD=PU+8.7 V  
    # starting at  Rd=Pu+8.5 we see a sensitivity (~ .0005 ) in the gain associated to // clock glithes 
    # So we take  RD<=PU+8 V as a constrain . Taking RD=PU+8 V allow to limit the shift down of the serial 
    # register when going to bi-polar , which is good for the noise.
    if RD_PU > 8.5 :
        print ("RD_PU =",RD_PU,' IS NOT A GOOD CHOICE (should be <=8.5) , Reset of the second stage amplifier will be incompleete , ending to gain instablity.') 
    RD=PU+RD_PU
    # OD : e2v requirement :  RD + 11 <  OD  , LSST addendum OD <~ RD + 12  for a good linearity 
    #  central values used by e2v  OD = RD + 12, proposed central value for an optimal linearity : OD = RD + 11.8 
    # Remark : OD = RD + 11.8  should be set at better than .1 V 
    OD=RD+11.8
    # RD ≥ OG + CHZ + 4V   ( E2V number )  ,  central values used by e2v OG = RD - 11 - 4 
    OG=RD - CHZ - 4
    if OG < OG_min :
        print('Optimal OG = ',OG,' is below allowed REB limit. It will be set to its allowed minimum ', OG_min,'(delta = ', OG_min-OG,' V) , to compute other parameters \n')
        if   OG_min-OG >= 1 :
            print('Still the difference between them is  > 1V , I consider this setup as bad !!!! \n')
        OG=OG_min
    # Serial low is then fixed by RD 
    # SL + 2.<  OG < SL + 4.5   ( E2V number)   
    # central value used by e2v  SL = OG - 2.5 
    # SL = OG - 2.  avoid to bring the serial too low in bipolar , no side effect of this choice so-far. 
    SL=OG-2.
    #  SU = Sswing + SL    
    SU = Sswing + SL
    # RGU > RD - 5.5     central values used by e2v  RGU =  RD - 5.5  , 
    #                    first stange amplifier seems to work  for RGU > RD - 6.3   and a swing of 10.7 V 
    # in practice the swing can be as low as 10. V , but better to get RGU = RD - 5.5 
    RGU = RD - 5.5
    RGL = RGU - RGswing 
    #  BSS target for diffusion and Brighter fatter   
    # based on the reference==> 60 V for PU = 9.3 V 
    # we could also add in the estimation the Pswing which can compensate for the BF  (to be done )
    BSS =  (BSS_ref - ( Pup_ref -Plow_ref ) / 2. ) + ( PU + PL) / 2.
    # GD should depend of BSS , for the moment we don't change it ... should ask e2v on what to do 
    GD=26
    # Print the result ========================================
    print ('====== Configuration ')
    print ('PU = %4.2f PL = %4.2f         ; Parallel Clocks Swing = %4.2f' % (PU,PL,PU-PL))
    print ('SU = %4.2f SL = %4.2f         ; Serial   Clocks Swing = %4.2f' % (SU,SL,SU-SL))
    print ('RGU= %4.2f RGL= %4.2f         ; Reset Gate      Swing = %4.2f' % (RGU,RGL,RGU-RGL))
    print ('OG = %4.2f                   ; remark SL should be kept <= OG -2 (=%4.2f V)    ' % (OG,OG-2.))
    print ('RD = %4.2f OD = %4.2f        ; remark OD-RD should be set to %4.2f V at better than 0.01 V ' % (RD,OD,OD-RD))
    print ('GD = %4.2f                   ; remark GD should be kept <= 26 V ' % (GD))
    print ('======\n')
    print ('Remark :\nBSS > %5.2f such BSS will have a contribution to PSF/diffusion and Brighter-Fatter effect of the same scale'  % (BSS))
    print ('than what was obtained in unipolar with BSS = %5.2f and Parallel up = %5.2f V and Parallel low =%5.2f V ' %(BSS_ref,Pup_ref,Plow_ref))
    return
