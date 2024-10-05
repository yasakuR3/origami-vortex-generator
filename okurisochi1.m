clearvars
close all
daq.reset()

s = daq.createSession('ni');
addAnalogInputChannel(s,'Dev1','ai0','Voltage');

s.Rate=20e3; % サンプリングレート 周波数
s.DurationInSeconds = 10; % ある一点における計測時間[s]
 
 nx=29; % x軸方向における測定個数
 dx=5; % x軸方向における測定間隔[mm]
 ny=13; % y軸方向における測定個数
 dy=5; % y軸方向における測定間隔[mm]

ser=[];

for j=0:(ny-1)
    for i=0:(nx-1)
      sx=sprintf('%02d',i), sy=sprintf('%02d',j);

        fn=['data_',sx,'_',sy,'_06.mat']

        data = startForeground(s);

         save(fn,'data');

        if i<(nx-1)
           ser=GP_two_axes_motor_drive(-dx,1,ser);%右向きに移動
        else
           ser=GP_two_axes_motor_drive(dx*(nx-1),1,ser);%左向きに戻る

           ser=GP_two_axes_motor_drive(dy, 0, ser);
         end
     end
end

% ser=GP_two_axes_motor_drive(dx*(nx-1),1,ser);%左向きに戻る

ser=GP_two_axes_motor_drive(-dy*ny, 0, ser);
