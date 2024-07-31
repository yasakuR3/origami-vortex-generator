clearvars
close all
daq.reset()

s = daq.createSession('ni');
addAnalogInputChannel(s,'Dev1','ai0','Voltage');

s.Rate=20e3; % サンプリングレート 周波数
s.DurationInSeconds =  0.5; % ある一点における計測時間[s]
 
 nx=11; % x軸方向における測定個数
 dx=10; % x軸方向における測定間隔[mm]
 ny=11; % y軸方向における測定個数
 dy=10; % y軸方向における測定間隔[mm]

ser=[];

for j=0:(ny-1)
    for i=0:(nx-1)
      sx=sprintf('%02d',i), sy=sprintf('%02d',j);

        fn=['data_',sx,'_',sy,'_01.mat']

        data = startForeground(s);

         save(fn,'data');

        if i<nx
           ser=GP_two_axes_motor_drive(-dx,1,ser);
        else
           ser=GP_two_axes_motor_drive(dx*(nx-1),1,ser);

           ser=GP_two_axes_motor_drive(-dy, 0, ser);
         end
     end
 end
