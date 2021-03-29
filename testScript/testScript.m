
% te=[];
% ye=[];
% ie=[];
% options = odeset('Events',@events,'NormControl','on','Refine',4,'AbsTol',1e-5,'Stats','on');
% [t,y]=ode45(@f,tspan,y0,options)
% sol=ode45(@f,tspan,y0,options)
% 
% 
% 
% plot(t,y(:,1))
% 
% fileID = fopen('test.txt','w');
% writetext(fileID, sol,tspan,y0,t,y,te,ye,ie)
% writetext(fileID,sol,tspan,y0,t,y,te,ye,ie)
% 
% function dydt = f(t,y,k)
% dydt = [y(2); -9.8];
% end
% 
% function [value,isterminal,direction] = events(t,y,k)
% % Locate the time when height passes through zero in a decreasing direction
% % and stop integration.
% value = [y(1),y(1)];     % detect height = 0
% isterminal = [1,1];   % stop the integration
% direction = [-1,-1];   % negative direction
% end


[fun,y0,tspan,varargin]=randInput('cosbasic',-100,100,0.05)
options=randTol(odeset(),y0);
%options=odeset()
[t,y]=ode45(@cosbasic,tspan,y0,options);
sol=ode45(@cosbasic,tspan,y0,options);
plot(t,y)

fileID = fopen('test.txt','w');
writetext(fileID, sol,tspan,y0,t,y,[],[],[])

function dydt = cosbasic(t,y)
    dydt=[cos(t);2*cos(t)];
end

function [fun,y0,tspan,varargin] = randInput(functions,start,en,space)
    bool = [0,1];
    if strcmp(functions,'cosbasic')
        fun=@cosbasic
        y0exponent = [1e0,1e1,1e2];
        y0=[rand * randsample(y0exponent,1); rand * randsample(y0exponent,1)];
        varargin = []
        if randsample(bool,1)
            t0= start + (en-start) .* rand;
            tend = t0 +(en-t0) .* rand;
            tspan = [t0,tend];
        elseif randsample(bool,1)
            t0= start + (en-start) .* rand;
            tend = t0 +(en-t0) .* rand;
            tspan = [t0:space:tend];
        else
            t0= start + (en-start) .* rand;
            tend = t0 +(en-t0) .* rand;
            num = round((t0-tend)/space)
            tspan=sort(rand(1,num))
        end
    end
end

function option = randTol(opt,y0)
    bool = [0,1];
    absexponent = [1e-10,1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3];
    relexponent = [1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1,1];
    randNorm=randsample(bool,1);
    if randNorm
        option=odeset(opt,'NormControl','on');
    else
        option=odeset(opt,'NormControl','off');
    end
    absArray=randsample(bool,1);
    if absArray && ~randNorm
        randAbs=rand(1,length(y0)).*randsample(absexponent,1);
    else
        randAbs=rand*randsample(absexponent,1);
    end
    option=odeset(option,'AbsTol',randAbs);
    option=odeset(option,'RelTol',rand*randsample(relexponent,1));
end



function writetext(fileID,sol,tspan,y0,t,y,te,ye,ie)
    
    %Inputs
    fprintf(fileID,'Function:');
    fprintf(fileID,'%s',func2str(sol.extdata.odefun));
    fprintf(fileID,' ');
    fprintf(fileID,'Tspan:');
    fprintf(fileID,'%.15f#',tspan);
    fprintf(fileID,' ');
    fprintf(fileID,'Y0:');
    fprintf(fileID,'%.15f#',y0);
    fprintf(fileID,' ');
    fprintf(fileID,'Varargin:');
    fprintf(fileID,'%.15f#',string(sol.extdata.varargin));
    fprintf(fileID,' ');
    
    %Options
    fprintf(fileID,'RelTol:');
    fprintf(fileID,'%.15f',sol.extdata.options.RelTol);
    fprintf(fileID,' ');
    fprintf(fileID,'AbsTol:');
    fprintf(fileID,'%.15f',sol.extdata.options.AbsTol);
    fprintf(fileID,' ');
    fprintf(fileID,'NormControl:');
    fprintf(fileID,'%s',sol.extdata.options.NormControl);
    fprintf(fileID,' ');
    fprintf(fileID,'Refine:');
    fprintf(fileID,'%d',sol.extdata.options.Refine);
    fprintf(fileID,' ');
    fprintf(fileID,'Stats:');
    fprintf(fileID,'%s',sol.extdata.options.Stats);
    fprintf(fileID,' ');
    fprintf(fileID,'NonNegative:');
    fprintf(fileID,'%d#',sol.extdata.options.NonNegative);
    fprintf(fileID,' ');
    fprintf(fileID,'Events:');
    if isa(sol.extdata.options.Events,'function_handle')
        fprintf(fileID,'%s',func2str(sol.extdata.options.Events));
    end
    fprintf(fileID,' ');
    fprintf(fileID,'MaxStep:');
    fprintf(fileID,'%.15f',sol.extdata.options.MaxStep);
    fprintf(fileID,' ');
    fprintf(fileID,'InitialStep:');
    fprintf(fileID,'%.15f',sol.extdata.options.InitialStep);
    fprintf(fileID,' ');
    fprintf(fileID,'Mass:');
    if isa(sol.extdata.options.Mass,'function_handle')
        fprintf(fileID,'%s',func2str(sol.extdata.options.Mass));
    else
        fprintf(fileID,'%.15f#',sol.extdata.options.Mass);
    end
    fprintf(fileID,' ');
    fprintf(fileID,'MStateDependence:');
    fprintf(fileID,'%s',sol.extdata.options.MStateDependence);
    fprintf(fileID,' ');

    %Output
    fprintf(fileID,'Tout:');
    fprintf(fileID,'%.15f#',t);
    fprintf(fileID,' ');
    fprintf(fileID,'Yout:');
    fprintf(fileID,'%.15f#',y);
    fprintf(fileID,' ');
    fprintf(fileID,'Nsteps:');
    fprintf(fileID,'%d',sol.stats.nsteps);
    fprintf(fileID,' ');
    fprintf(fileID,'Nfailed:');
    fprintf(fileID,'%d',sol.stats.nfailed);
    fprintf(fileID,' ');
    fprintf(fileID,'Nfevals:');
    fprintf(fileID,'%d',sol.stats.nfevals);
    fprintf(fileID,' ');
    fprintf(fileID,'Teout:');
    if isa(sol.extdata.options.Events,'function_handle')
        fprintf(fileID,'%.15f#',te);
    end
    fprintf(fileID,' ');
    fprintf(fileID,'Yeout:');
    if isa(sol.extdata.options.Events,'function_handle')
        fprintf(fileID,'%.15f#',ye);
    end
    fprintf(fileID,' ');
    fprintf(fileID,'Ieout:');
    if isa(sol.extdata.options.Events,'function_handle')
        fprintf(fileID,'%d#',ie);
    end
    fprintf(fileID,'\n');
    
end