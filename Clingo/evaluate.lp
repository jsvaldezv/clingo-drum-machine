% THEN EVALUATE

% sound(instrument,answerSet,centroid,spread,peak,).
%sound(kick,1,900,500,300).
%sound(kick,2,800,520,301).
%sound(kick,3,700,530,302).
%sound(kick,4,950,600,320).
%sound(kick,5,910,400,301).

%sound(hihat,1,10000,7000,12000).
%sound(hihat,2,8000,7500,11002).
%sound(hihat,3,9000,8000,12502).
%sound(hihat,4,9500,8500,15005).
%sound(hihat,5,9100,9000,14007).

%sound(snare,1,4000,0,0).
%sound(snare,2,3000,0,0).
%sound(snare,3,2000,0,0).
%sound(snare,4,1000,0,0).
%sound(snare,5,6000,0,0).

%% Sum the centroid and peak of each kick, and then choose the lowest.
sumKick(N, S) :- sound(kick, N, X, Y, Z), S = X+Z.
1 { betterKick(kick, N,S) : sumKick(N, S) } 1.
#minimize {S, N : betterKick(kick, N, S)}.

%% Sum the centroid and peak of each hi-hat, and then choose the highest.
sumHihat(N, S) :- sound(hihat, N, X, Y, Z), S = X+Z.
1 { betterHihat(hihat, N,S) : sumHihat(N, S) } 1.
#maximize {S, N : betterHihat(hihat, N, S)}.

%% Chose the snare with the largest spread (presence).
sumSnare(N, S) :- sound(snare, N, X, Y, Z), S = Y.
1 { betterSnare(snare, N,S) : sumSnare(N, S) } 1.
#maximize {S, N : betterSnare(snare, N, S)}.

#show betterKick/3.
#show betterHihat/3.
#show betterSnare/3.