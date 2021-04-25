
function main()
    fileID = fopen('ode.txt','w');
    
% %     Poly NN with nonnegative
%     opt=odeset('NonNegative',[1,2])
%     tspan = [-6,5]
%     y0=[25,50,25,50]
%     [t,y]=ode45(@polyNN,tspan,y0,opt);
%     sol=ode45(@polyNN,tspan,y0,opt);
%     
%     writetext(fileID,sol,tspan,y0,t,y,[],[],[]);
%     
% %     Ball ode
%     y0 = [0;20];
%     tspan = [0,30];
%     opt = odeset('Events',@ballevents);
%     [t,y,te,ye,ie] = ode45(@ball,tspan,y0,opt)
%     sol=ode45(@ball,tspan,y0,opt);
%     %disp(sol.stats)
%     %plot(t,y)
%     
%     writetext(fileID,sol,tspan,y0,t,y,te,ye,ie);
% 
% %     Trig events
%     y0 = [0;-1];
%     tspan = [0,30];
%     opt = odeset('Events',@trigevents);
%     [t,y,te,ye,ie] = ode45(@trigbasic,tspan,y0,opt);
%     sol=ode45(@trigbasic,tspan,y0,opt);
%     %plot(t,y)
%     %hold on;
%     %disp(ye(:,1))
%     %scatter(te,ye(:,1))
%     %scatter(te,ye(:,2))
    
    %writetext(fileID,sol,tspan,y0,t,y,te,ye,ie);
    
    
    opt=odeset('RelTol' , 0.0009,'AbsTol' , 3.e-5,'NormControl' , 'on','Refine' , 3,'NonNegative' , [1, 2]);
    tspan = [19, 53];
    y0 = [6; 38];

    [t,y]=ode45(@trigbasic2,tspan,y0,opt);
    sol=ode45(@trigbasic2,tspan,y0,opt);
    writetext(fileID,sol,tspan,y0,t,y,[],[],[]);
    
end


%%

function dydt = polyNN(t,y)
    dydt = [0.02*(3*t^5-62*t^3+42*t^2+45*t+18);0.02*(3*t^5-62*t^3+42*t^2+45*t+18);0.02*(3*t^5-62*t^3+42*t^2+45*t+18);0.02*(3*t^5-62*t^3+42*t^2+45*t+18)]
end

function dydt = ball(t,y)
dydt = [y(2); -9.8];
end

function dydt = trigbasic(t,y)
    dydt = [cos(t);sin(t)];
end

function dydt = trigbasic2(t,y)
    dydt = [y(1)*cos(t);y(2)*sin(t)];
end

function [value,isterminal,direction] = ballevents(t,y)
value = [y(1)];
isterminal = [1];
direction = [-1];
end

function [value,isterminal,direction] = trigevents(t,y)
value = [y(1),y(2),y(1)];
isterminal = [0,0,0];
direction = [-1,0,1];
end


%%

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
    fprintf(fileID,'%.15f#',sol.extdata.options.AbsTol);
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