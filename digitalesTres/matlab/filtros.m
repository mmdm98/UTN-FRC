%TP1
%Delgadillo Marcos
%75196

%Filtro 1kHz
num1=[628];
den1=[1 628];

filtro1=tf(num1,den1);
bode(filtro1);
grid();
hold();

%Filtro 10Hz
num2=[62.8];
den2=[1 62.8];

filtro2=tf(num2,den2);
bode(filtro2);
grid();

multi=filtro1*filtro2;
bode(multi);
grid();

%title("Filtros");
legend("1000Hz","10Hz","Mult");