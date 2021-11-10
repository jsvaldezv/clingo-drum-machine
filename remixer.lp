% FIRST REMIX

%% Audio
%% 400 ms
sound(kick).
sound(snare).
sound(hihat).

%% Frequency Ranges (¿centroide espectral de cada ventana?)


%% Envelope parameters

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

elsobre(N,A,R):- attack(N,A),release(N,R).

#show elsobre/3.



%% FX Selection Section



