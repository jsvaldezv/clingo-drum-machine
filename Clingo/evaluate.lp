% THEN EVALUATE

% sound(instrument,answerSet,centroid,spread,peak,).
sound(kick,1,900,500,300).
sound(kick,2,800,520,301).
sound(kick,3,700,530,302).
sound(kick,4,950,600,320).
sound(kick,5,900,400,301).

% sumKick(S,N) :- S = X + Y + Z, sound(kick,N,X,Y,Z).
#minimize { S : sound(kick,_,X,Y,Z), S = X + Y + Z }.

#show sumKick/2.