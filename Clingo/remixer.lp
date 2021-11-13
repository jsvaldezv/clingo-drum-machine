% **************** Audio ****************
sound(kick).
sound(snare).
sound(hihat).

% **************** Envelope parameters ****************
1 { kickAttack(1) ; kickAttack(3) ; kickAttack(5)  } 1 :- sound(kick).
1 { snareAttack(1) ; snareAttack(3) ; snareAttack(5)  } 1 :- sound(snare).
1 { hihatAttack(1) ; hihatAttack(3) ; hihatAttack(5)  } 1 :- sound(hihat).

attack(kick,A) :- kickAttack(A).
attack(snare,A) :- snareAttack(A).
attack(hihat,A) :- hihatAttack(A).

1 { kickRel(1) ; kickRel(3) ; kickRel(5)  } 1 :- sound(kick).
1 { snareRel(1) ; snareRel(3) ; snareRel(5)  } 1 :- sound(snare).
1 { hihatRel(1) ; hihatRel(3) ; hihatRel(5)  } 1 :- sound(hihat).

release(kick,R) :- kickRel(R).
release(snare,R) :- snareRel(R).
release(hihat,R) :- hihatRel(R).

envelope(N,A,R):- attack(N,A),release(N,R).

% **************** Rhythms ****************
1 { rKick(1; 2) } 1 :- sound(kick).
1 { rSnare(1; 2) } 1 :- sound(snare).
1 { rHihat(1; 2) } 1 :- sound(hihat).

rhythm(kick,R) :- rKick(R).
rhythm(snare,R) :- rSnare(R).
rhythm(hihat,R) :- rHihat(R).

% **************** FX Selection Section ****************
1 { pitchKick(-1200); pitchKick(-1800); pitchKick(-2400) } 1 :- sound(kick). % Cents
1 { eqKick(1000); eqKick(1700); eqKick(3000) } 1 :- sound(kick). % LPF

pitchSnare(0) :- sound(snare).
1 { eqSnare(100); eqSnare(200); eqSnare(300) } 1 :- sound(snare). % HPF

1 { pitchHihat(1200); pitchHihat(1800); pitchHihat(2400) } 1 :- sound(hihat). % Cents
1 { eqHihat(300); eqHihat(500); eqHihat(700) } 1 :- sound(hihat). % HPF

fx(kick,P,E) :- pitchKick(P), eqKick(E).
fx(snare,P,E) :- pitchSnare(P), eqSnare(E).
fx(hihat,P,E) :- pitchHihat(P), eqHihat(E).

% **************** Result ****************
design(I,A,R,Rh,P,E) :- envelope(I,A,R), rhythm(I,Rh), fx(I,P,E).
#show design/6.