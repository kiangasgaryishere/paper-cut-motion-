"""Original instrumental for the carpet film. All instruments are synthesized."""
import numpy as np
from scipy.signal import butter, sosfilt

# D-centered melody. Each event is (beat within the bar, scale degree, held beats).
# The lowered second and raised third give the phrases their Hijaz-like contour.
PHRASES = (
    (((0,0,.7),(1,1,.4),(1.5,2,.7),(2.5,3,.9)), ((0,2,1),(1.5,1,.4),(2,0,1.2))),
    (((0,2,.7),(1,3,.4),(1.5,4,1.05),(3,3,.5)), ((0,2,.6),(1,1,.55),(2,0,1.4))),
    (((0,3,1),(1.5,4,.5),(2,5,.5),(2.5,4,.8)), ((0,3,.75),(1,1,.6),(2,0,1.4))),
    (((0,0,.85),(1.5,1,.4),(2,2,.5),(3,1,.5)), ((0,0,1.9),)),
    (((0,4,.8),(1,3,.6),(2,2,1.25)), ((0,1,.65),(1,-1,.55),(2,0,1.6))),
    (((0,2,.9),(1.5,3,.45),(2,2,.65),(3,1,.5)), ((0,0,2.3),)),
)
INTERVALS = (0, 1, 4, 5, 7, 8, 10)

def note_hz(degree, octave, cents=0):
    register, index = divmod(degree, len(INTERVALS))
    midi = 50 + INTERVALS[index] + 12*(register+octave)
    return 440*2**((midi-69+cents/100)/12)

def make_score(rate, samples):
    rng=np.random.default_rng(519)
    music=np.zeros((samples,2),np.float32)
    beat=60/103
    def place(x, seconds, gain, pan):
        i=round(seconds*rate)
        x=x[:max(0,min(len(x),samples-i))]
        music[i:i+len(x)]+=x[:,None]*gain*np.sqrt([(1-pan)/2,(1+pan)/2])

    def strings(degree, octave, hold, hammered, cents=0):
        duration=hold*beat+(.38 if hammered else .29)
        t=np.arange(round(duration*rate))/rate
        f=note_hz(degree,octave,cents)
        signal=np.zeros_like(t)
        # Detuned courses and independently decaying partials suggest paired strings.
        detunes=(-.0021,.0014) if hammered else (-.003,.002)
        for detune in detunes:
            x=t+(.00085 if hammered else .0015)*np.sin(2*np.pi*4.5*t)
            for partial in range(1,9):
                brightness=partial**(-1.18 if hammered else -1.43)
                stiff=1+(.00024 if hammered else .000085)*partial**2
                decay=(3.0 if hammered else 4.4)+partial*.91
                signal+=brightness*np.sin(2*np.pi*f*(1+detune)*partial*stiff*x+rng.uniform(0,.35))*np.exp(-t*decay)
        # Short plectrum or mallet transient.
        noise=sosfilt(butter(2,[750,3600],btype='bandpass',fs=rate,output='sos'),rng.normal(0,1,t.size))
        signal+=noise*np.exp(-t*130)*(.13 if hammered else .23)
        signal*=np.minimum(1,t/.009)*np.minimum(1,np.maximum(0,(duration-t)/.17))
        return signal/(np.max(np.abs(signal))+1e-9)

    def drum(low):
        t=np.arange(round(rate*.19))/rate
        f=83 if low else 185
        body=np.sin(2*np.pi*(f*t+24*t*np.exp(-t*25)))*np.exp(-t*(27 if low else 52))
        grit=sosfilt(butter(2,[260,3100],btype='bandpass',fs=rate,output='sos'),rng.normal(0,1,t.size))
        return (body+grit*.72*np.exp(-t*56))*np.minimum(1,t/.004)

    start=.14
    # Six original phrases are arranged in sections, with a sparser middle
    # for Origin/Design and a light return under the final question.
    order=[0,1,2,0,4,1,3,5,3,0,2,4,1,0,3,5,0,1,3,5]
    for j,phrase in enumerate(order):
        section=start+j*8*beat
        sparse=39<section<58
        for bar,phrase_bar in enumerate(PHRASES[phrase]):
            bar_time=section+bar*4*beat
            for offset,degree,hold in phrase_bar:
                # E-half-flat variation in quieter answering phrases.
                cents=38 if degree==1 and phrase in (2,4) else 0
                place(strings(degree,1,hold,True,cents),bar_time+offset*beat,.145 if sparse else .18,-.29)
            bass=0 if bar else (4 if phrase in (1,4) else 0)
            for off,degree,volume in [(0,bass,.17),(1.5,0,.10),(2.5,4,.10),(3.5,0,.08)]:
                if sparse and off in (1.5,3.5):
                    continue
                place(strings(degree,0,.87,False),bar_time+off*beat+.022,volume,.32)
            for off,low,volume in [(0,True,.105),(1.5,False,.068),(2.5,False,.051),(3,True,.073)]:
                if not sparse:
                    place(drum(low),bar_time+off*beat,volume,.09)
    # Short stereo room taps. Independent of the narration.
    stereo=music.copy()
    for delay,gain in [(.061,.095),(.108,.071),(.159,.052)]:
        n=round(rate*delay)
        music[n:]+=stereo[:-n,::-1]*gain
    music[:int(rate*.5)]*=np.linspace(0,1,int(rate*.5))[:,None]
    end=round(rate*1.3)
    music[-end:]*=np.linspace(1,0,end)[:,None]
    return music
