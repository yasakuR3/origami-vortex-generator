clearvars
close all
daq.reset()

s = daq.createSession('ni');
addAnalogInputChannel(s,'Dev1','ai0','Voltage');

s.Rate=20e3; % サンプリングレート 周波数
s.DurationInSeconds = 1;%サンプリングタイム　ある一点における計測時間 計測時間を長くすることでノイズの影響を少なくできる。
 
 nx=10;
 dx=10;
 ny=10;
 dy=10;

ser=[];

for j=1:ny
    for i=1:nx
      sy=sprintf('%02d',j);
       sx=sprintf('%02d',i);
        fn=['data_',sy,'_',sx,'_01.mat']

        data = startForeground(s);

         save(fn,'data');

        if i<nx
           ser=GP_two_axes_motor_drive(-dx,1,ser);
        else
             ser=GP_two_axes_motor_drive(dx*(nx-1),1,ser);

         end
 
     end
     if j<ny
         ser=GP_two_axes_motor_drive(-dy,0,ser);

     else
         ser=GP_two_axes_motor_drive(dy*(ny-3),0,ser);
     end
 end
