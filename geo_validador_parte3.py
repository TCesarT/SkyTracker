from manageBD import cargarBD


def validar_ubicacion():
  data = cargarBD()
  estados = data["ubicaciones_validas"]

  print("Validación de ubicación:")

  while True:
    edo = input("Estado (escriba LISTAR para ver opciones): ").strip()
    if edo.upper() == "LISTAR":
      for e in estados:
        print("-", e)
      continue

    edo = " ".join(edo.split()).title()
    if edo in estados:
      break
    print("Estado no válido.")

  while True:
    muni = input(f"Municipio para {edo} (escriba LISTAR para ver): ").strip()
    if muni.upper() == "LISTAR":
      for m in estados[edo]:
        print("-", m)
      continue

    muni = " ".join(muni.split()).title()
    if muni in estados[edo]:
      return edo, muni
    print("El municipio no pertenece a este estado.")


if __name__ == "__main__":
  validar_ubicacion()
