import os
import re
import pywhatkit as kit
import smtplib
from email.mime.text import MIMEText

def mostrar_menu():
  print("1. Registrar información")
  print("2. Ver información")
  print("3. Actualizar información")
  print("4. Salir")

def validar_dato(dato, tipo):
  if tipo == "nombre":
    return re.match("^[A-Za-z]+$", dato)
  elif tipo == "fecha":
    return re.match("^\d{2}/\d{2}/\d{4}$", dato)
  elif tipo == "correo":
    return re.match(r"[^@]+@[^@]+\.[a-zA-Z]{2,}$", dato)
  elif tipo == "telefono":
    return re.match("^\+\d{10,15}$", dato)
  else:
    return False

def registrar_informacion():
  nombre = input("Nombre: ")
  if not validar_dato(nombre, "nombre"):
    print("Nombre inválido.")
    return

  apellido = input("Apellido: ")
  if not validar_dato(apellido, "nombre"):
    print("Apellido inválido.")
    return

  fecha_nacimiento = input("Fecha de nacimiento (DD/MM/AAAA): ")
  if not validar_dato(fecha_nacimiento, "fecha"):
    print("Fecha de nacimiento inválida.")
    return

  pais = input("País: ")
  correo = input("Correo: ")
  if not validar_dato(correo, "correo"):
    print("Correo electrónico inválido.")
    return

  numero_telefonico = input("Número telefónico con tu codigo de pais (+): ")
  if not validar_dato(numero_telefonico, "telefono"):
    print("Número telefónico inválido.")
    return

  with open("informacion.txt", "a") as archivo:
    archivo.write(f"{nombre},{apellido},{fecha_nacimiento},{pais},{correo},{numero_telefonico}\n")
  print("Información registrada con éxito.")
  enviar_bienvenida(numero_telefonico, correo,15)

def enviar_bienvenida(numero, correo):
  try:
    kit.sendwhatmsg_instantly(numero, "¡Bienvenido! Gracias por registrarte.", 15)
    enviar_email(correo, "¡Bienvenido!", "Gracias por registrarte.")
    print("Mensaje de bienvenida enviado.")
  except Exception as e:
    print(f"Error al enviar mensaje de bienvenida: {e}")

def enviar_email(destinatario, asunto, mensaje):
  remitente = "angelgap1112@gmai.com"
  password = "ovop bmok dbcb hwmh"
  msg = MIMEText(mensaje)
  msg["Subject"] = asunto
  msg["From"] = remitente
  msg["To"] = destinatario

  try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(remitente, password)
    server.sendmail(remitente, [destinatario], msg.as_string())
    server.quit()
  except Exception as e:
    print(f"Error al enviar correo electrónico: {e}")

def ver_informacion():
  if os.path.exists("informacion.txt"):
    with open("informacion.txt", "r") as archivo:
      for linea in archivo:
        print(linea.strip())
  else:
    print("No hay información registrada.")

def actualizar_informacion():
  if os.path.exists("informacion.txt"):
    nombre = input("Nombre de la persona a actualizar: ")
    lineas = []
    with open("informacion.txt", "r") as archivo:
      lineas = archivo.readlines()

    with open("informacion.txt", "w") as archivo:
      for linea in lineas:
        if linea.startswith(nombre):
          print("Ingrese la nueva información:")
          nuevo_nombre = input("Nombre: ")
          nuevo_apellido = input("Apellido: ")
          nueva_fecha_nacimiento = input("Fecha de nacimiento (DD/MM/AAAA): ")
          nuevo_pais = input("País: ")
          nuevo_correo = input("Correo: ")
          nuevo_numero_telefonico = input("Número telefónico: ")
          archivo.write(f"{nuevo_nombre},{nuevo_apellido},{nueva_fecha_nacimiento},{nuevo_pais},{nuevo_correo},{nuevo_numero_telefonico}\n")
        else:
          archivo.write(linea)
        print("Información actualizada con éxito.")
  else:
    print("No hay información registrada.")

def main():
  while True:
    mostrar_menu()
    opcion = input("Seleccione una opción: ")
    if opcion == "1":
      registrar_informacion()
    elif opcion == "2":
      ver_informacion()
    elif opcion == "3":
      actualizar_informacion()
    elif opcion == "4":
      break
    else:
      print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
  main()
