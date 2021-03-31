
function main()
    fun = @cosbasic;
    size = 2;
    tstart=-100;
    tend=100;
    y0start=1;
    y0end=100;
    events=@eventsbasic;
    mass=[];
    
    choices={'tol','refine','nonnegative','step'};
    fileID = fopen('test.txt','w');
    execute_test(fun,size,tstart,tend,y0start,y0end,events,mass,choices,fileID)
    
    
%     choices={};
%     fileID = fopen('basictest.txt','w');
%     execute_test(fun,size,tstart,tend,y0start,y0end,events,mass,choices,fileID)
%     
%     choices={'tol'};
%     fileID = fopen('toltest.txt','w');
%     execute_test(fun,size,tstart,tend,y0start,y0end,events,mass,choices,fileID)
%     
%     choices={'refine'};
%     fileID = fopen('refinetest.txt','w');
%     execute_test(fun,size,tstart,tend,y0start,y0end,events,mass,choices,fileID)
%     
%     choices={'nonnegative'};
%     fileID = fopen('nntest.txt','w');
%     execute_test(fun,size,tstart,tend,y0start,y0end,events,mass,choices,fileID)
%     
%     choices={'step'};
%     fileID = fopen('basic.txt','w');
%     execute_test(fun,size,tstart,tend,y0start,y0end,events,mass,choices,fileID)
%     
%     choices={'events'};
%     fileID = fopen('eventstest.txt','w');
%     execute_test(fun,size,tstart,tend,y0start,y0end,events,mass,choices,fileID)
%     
%     choices={'massmatrix'};
%     fileID = fopen('massmatrixtest.txt','w');
%     execute_test(fun,size,tstart,tend,y0start,y0end,events,mass,choices,fileID)
%     
%     choices={};
%     fileID = fopen('alltest.txt','w');
%     execute_test(fun,size,tstart,tend,y0start,y0end,events,mass,choices,fileID)
    
end

function execute_test(fun,size,tstart,tend,y0start,y0end,events,mass,choices,textfile)
    succ = false;
    while ~succ
        [y0,tspan]=randInput(size,tstart,tend,y0start,y0end);
        options = odeset();
        te=[];
        ye=[];
        ie=[];
        if any(strcmp(choices,'tol'))
            options = randTol(options,y0);
        end
        if any(strcmp(choices,'refine'))
            options = randRefine(options);
        end
        if any(strcmp(choices,'nonnegative'))
            options = randNN(options,y0);
        end
        if any(strcmp(choices,'step'))
            options = randStep(options);
        end
        if any(strcmp(choices,'events'))
            options = odeset(options,'Events',events);
        end
        if any(strcmp(choices,'massmatrix'))
            options = randMatrix(options,y0);
        end
        if any(strcmp(choices,'massfunctime'))
            options = odeset(options,'Events',mass,'MStateDependence','none');
        end
        if any(strcmp(choices,'massfuncstate'))
            options = odeset(options,'Mass',mass,'MStateDependence','weak');
        end
        try
            if any(strcmp(choices,'events'))
                [t,y,te,ye,ie]=ode45(@cosbasic,tspan,y0,options);
            else
                [t,y]=ode45(@cosbasic,tspan,y0,options);
            end
            sol=ode45(@cosbasic,tspan,y0,options);
            succ = true;
        catch
            warning('Test failed');
        end
    end
    plot(t,y)
    writetext(textfile,sol,tspan,y0,t,y,te,ye,ie);
end



%%
%
%   Write your functions/mass functions here
%
%

function dydt = cosbasic(t,y)
    dydt=[cos(t);2*cos(t)];
end

function [value,isterminal,direction] = eventsbasic(t,y)
    value = [y(1),y(2)];
    isterminal = [1,0];
    direction = [1,-1];
end

%%



%%
function [y0,tspan] = randInput(size,start,en,y0start,y0end)
    bool = [0,1];
    y0exponent = zeros(1,floor(log10(y0end/y0start))+1);
    y0exponent(1) = y0start;
    for i = 2:length(y0exponent)
        y0exponent(i) = y0exponent(i-1)*10;
    end
    y0=zeros(size,1);
    for i=1:size
        y0(i) = rand * randsample(y0exponent,1);
    end
    if randsample(bool,1)
        t0= start + (en-start) .* rand;
        tend = t0 +(en-t0) .* rand;
        tspan = [t0,tend];
    elseif randsample(bool,1)
        t0= start + (en-start) .* rand;
        tend = t0 +(en-t0) .* rand;
        space = 1/ (50 + (1000-50) *rand);
        tspan = [t0:space:tend];
    else
        t0= start + (en-start) .* rand;
        tend = t0 +(en-t0) .* rand;
        space = 1 / (50 + (1000-50) *rand);
        num = round((tend-t0)/space);
        tspan=sort(rand(1,num)*(tend-t0) + t0);
        
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

function option = randRefine(opt)
    option = odeset(opt,'Refine',floor(1 + 20 * rand));
end

function option = randNN(opt,y0)
    bool = [0,1];
    size = length(y0);
    index = [];
    for i = 1:size
        if randsample(bool,1)
            index = [index, i];
        end
    end
    option = odeset(opt,'NonNegative',index);
end

function option = randStep(opt)
    maxexponent = [1e-3,1e-2,1e-1,1,10];
    initexponent = [1e-5,1e-4,1e-3,1e-2,1e-1,1];
    option=odeset(opt,'MaxStep',rand*randsample(maxexponent,1));
    option=odeset(option,'InitialStep',rand*randsample(initexponent,1));
end


function option = randMatrix(opt,y0)
    massexponent = [,1e-1,1,1e1];
    size = length(y0);
    mat = zeros(size,size);
    for i = 1:size
        for j = 1:size
            mat(i,j)=rand*randsample(massexponent,1);
        end
    end
    disp(mat)
    option = odeset(opt,'Mass',mat);
end


%%

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