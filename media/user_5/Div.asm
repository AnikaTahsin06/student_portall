  include 'emu8086.inc'
  
 mov ah,1
 int 21h
 mov bl,al
 sub bl,48
 
 mov ah,1
 int 21h
 mov cl,al
 sub cl,48
 
 mov al,0
 mov ah,0
 
 mov al,bl
 div cl
 
 mov bl,ah
 mov cl,al
 mov dl,bl
 add dl,48
 
 mov ah,2
 int 21h
 
 mov dl,cl
 add dl,48
 mov ah,2
 int 21h
 
 