############################################################################################
#															 															                                                                  
#  					Imagem Base Para Execução de Modelo Analítico               
#  				      Criado por Sérgio Valle Júnior                 
#  					Data: 28/02/2021                     
#															 
############################################################################################
############################################################################################
#															 
# Definição da Imagem Base a Ser Utilizada - Imagem da Microsoft Já com 
# Anaconda Instalado, IIS configurado                                               	 
#															 
############################################################################################
FROM sergiovallejr/windows-server-core-anaconda-iis-ml:1.3
############################################################################################
#															 
# Adiciona o Label a nova imagem                                                    	 
#									                                     
############################################################################################
LABEL key="APP BASE"
############################################################################################
#																						   
# Cria ambiente do conda                                      				               
#																						   
############################################################################################
ADD ./env/base-env.yml /inetpub/wwwroot
RUN powershell -Command \
	Invoke-Command -ScriptBlock {conda clean --all --yes};\
	Invoke-Command -ScriptBlock {conda env update -f c:\inetpub\wwwroot\base-env.yml --prune};\
	Invoke-Command -ScriptBlock {conda clean --all --yes}
############################################################################################
# Adiciona o arquivo de polyces do windows
############################################################################################
ADD ./docker/app/policies.inf /inetpub/wwwroot
RUN secedit /configure /db %windir%\security\local.sdb /cfg c:\inetpub\wwwroot\policies.inf
###########################################################################################
COPY ["./docker/bin/LogMonitor.exe", \
      "./docker/bin/LogMonitorConfig.json", \
      "./LogMonitor/"]
WORKDIR /LogMonitor
# Change the startup type of the IIS service from Automatic to Manual
RUN sc config w3svc start=demand    
# Enable ETW logging for Default Web Site on IIS
###########################################################################################
#
# Adiciona e Seta propriedades do IIS, FastCGI e Pool de Aplicativos
#
###########################################################################################
RUN c:\windows\system32\inetsrv\appcmd.exe set config -section:system.applicationHost/sites /"[name='Default Web Site'].logFile.logTargetW3C:"File,ETW"" /commit:apphost
RUN powershell -Command \
   Import-Module WebAdministration ; \
   Set-WebConfigurationProperty -pspath 'MACHINE/WEBROOT/APPHOST'  -filter 'system.webServer/fastCgi/application[@fullPath=''C:\anaconda\python.exe'']' -name 'idleTimeout' -value 7200 ; \
   Set-ItemProperty 'IIS:\AppPools\DefaultAppPool' -Name startMode -Value 'alwaysrunning' ; \
   Set-ItemProperty 'IIS:\AppPools\DefaultAppPool' -Name processModel.idleTimeout -Value ([TimeSpan]::FromMinutes(120)) ; \
   Set-ItemProperty 'IIS:\AppPools\DefaultAppPool' -name processModel -value @{userName='User03';password='123XYab';identitytype=3} ; \
   Set-ItemProperty 'IIS:\Sites\Default Web Site' -Name applicationDefaults.preloadEnabled -Value True
############################################################################################
#																						   
# Adiciona código à Imagem                                  				             
#																						  
############################################################################################
ADD . /inetpub/wwwroot/
############################################################################################
# Start "C:\LogMonitor\LogMonitor.exe C:\ServiceMonitor.exe w3svc"
ENTRYPOINT ["C:\\LogMonitor\\LogMonitor.exe", "C:\\ServiceMonitor.exe", "w3svc"]