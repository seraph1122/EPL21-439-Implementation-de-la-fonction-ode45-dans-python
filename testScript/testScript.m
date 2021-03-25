y0 = [0;20];
tspan=[0 10];
te=[];
ye=[];
ie=[];
options = odeset();%'Events',@events,'NormControl','on','Refine',4,'Stats','on');
[t,y]=ode45(@f,tspan,y0,options)
sol=ode45(@f,tspan,y0,options)



plot(t,y(:,1))

fileID = fopen('test.txt','w');
writetext(fileID, sol,tspan,y0,t,y,te,ye,ie)
writetext(fileID,sol,tspan,y0,t,y,te,ye,ie)

function dydt = f(t,y)
dydt = [y(2); -9.8];
end

function [value,isterminal,direction] = events(t,y)
% Locate the time when height passes through zero in a decreasing direction
% and stop integration.
value = [y(1),y(1)];     % detect height = 0
isterminal = [1,1];   % stop the integration
direction = [-1,-1];   % negative direction
end

function writetext(fileID,sol,tspan,y0,t,y,te,ye,ie)
    %fileID = fopen('test.txt','w');
    
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


% function writetext(sol,tspan,y0,t,y,te,ye,ie)
%     fileID = fopen('test.txt','w');
%     
%     fprintf(fileID,'New');
%     %Inputs
%     fprintf(fileID,'Function\n');
%     fprintf(fileID,'%s',func2str(sol.extdata.odefun));
%     fprintf(fileID,'\n');
%     fprintf(fileID,'Tspan\n');
%     fprintf(fileID,'%f ',tspan);
%     fprintf(fileID,'\n');
%     fprintf(fileID,'Y0\n');
%     fprintf(fileID,'%f ',y0);
%     fprintf(fileID,'\n');
%     fprintf(fileID,'Varargin\n');
%     fprintf(fileID,'%f ',string(sol.extdata.varargin));
%     fprintf(fileID,'\n');
%     
%     %Options
%     fprintf(fileID,'RelTol\n');
%     fprintf(fileID,'%f',sol.extdata.options.RelTol);
%     fprintf(fileID,'\n');
%     fprintf(fileID,'AbsTol\n');
%     fprintf(fileID,'%f',sol.extdata.options.AbsTol);
%     fprintf(fileID,'\n');
%     fprintf(fileID,'NormControl\n');
%     fprintf(fileID,'%s',sol.extdata.options.NormControl);
%     fprintf(fileID,'\n');
%     fprintf(fileID,'Refine\n');
%     fprintf(fileID,'%d',sol.extdata.options.Refine);
%     fprintf(fileID,'\n');
%     fprintf(fileID,'Stats\n');
%     fprintf(fileID,'%s',sol.extdata.options.Stats);
%     fprintf(fileID,'\n');
%     fprintf(fileID,'NonNegative\n');
%     fprintf(fileID,'%d ',sol.extdata.options.NonNegative);
%     fprintf(fileID,'\n');
%     fprintf(fileID,'Events\n');
%     if isa(sol.extdata.options.Events,'function_handle')
%         fprintf(fileID,'%s',func2str(sol.extdata.options.Events));
%     else
%         fprintf(fileID,'\n');
%     end
%     fprintf(fileID,'\n');
%     fprintf(fileID,'MaxStep\n');
%     fprintf(fileID,'%f',sol.extdata.options.MaxStep);
%     fprintf(fileID,'\n');
%     fprintf(fileID,'InitialStep\n');
%     fprintf(fileID,'%f',sol.extdata.options.InitialStep);
%     fprintf(fileID,'\n');
%     fprintf(fileID,'Mass\n');
%     if isa(sol.extdata.options.Mass,'function_handle')
%         fprintf(fileID,'%s',func2str(sol.extdata.options.Mass));
%     else
%         fprintf(fileID,'%f',sol.extdata.options.Mass);
%     end
%     fprintf(fileID,'\n');
%     fprintf(fileID,'MStateDependence\n');
%     fprintf(fileID,'%s',sol.extdata.options.MStateDependence);
%     fprintf(fileID,'\n');
% 
%     %Output
%     fprintf(fileID,'Tout\n');
%     fprintf(fileID,'%f ',t);
%     fprintf(fileID,'\n');
%     fprintf(fileID,'Yout\n');
%     fprintf(fileID,'%f ',y);
%     fprintf(fileID,'\n');
%     fprintf(fileID,'Nsteps\n');
%     fprintf(fileID,'%d',sol.stats.nsteps);
%     fprintf(fileID,'\n');
%     fprintf(fileID,'Nfailed\n');
%     fprintf(fileID,'%d',sol.stats.nfailed);
%     fprintf(fileID,'\n');
%     fprintf(fileID,'Nfevals\n');
%     fprintf(fileID,'%d',sol.stats.nfevals);
%     fprintf(fileID,'\n');
%     fprintf(fileID,'Teout\n');
%     if isa(sol.extdata.options.Events,'function_handle')
%         fprintf(fileID,'%s',te);
%     else
%         fprintf(fileID,'\n');
%     end
%     fprintf(fileID,'\n');
%     fprintf(fileID,'Yeout\n');
%     if isa(sol.extdata.options.Events,'function_handle')
%         fprintf(fileID,'%f ',ye);
%     else
%         fprintf(fileID,'\n');
%     end
%     fprintf(fileID,'\n');
%     fprintf(fileID,'Ieout\n');
%     if isa(sol.extdata.options.Events,'function_handle')
%         fprintf(fileID,'%d ',ie);
%     else
%         fprintf(fileID,'\n');
%     end
%     fprintf(fileID,'\n');
%     
% end