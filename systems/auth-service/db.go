package main

import (
	"database/sql"
	"log"

	_ "modernc.org/sqlite"
)

var db *sql.DB

func InitDB() {
	var err error
	db, err = sql.Open("sqlite", "./auth.db")
	if err != nil {
		log.Fatal(err)
	}

	createTables := `
        CREATE TABLE IF NOT EXISTS rol (
            idrol INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS usuario (
            idusuario INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            rol_id INTEGER,
            FOREIGN KEY (rol_id) REFERENCES rol(idrol)
        );`
	_, err = db.Exec(createTables)
	if err != nil {
		log.Fatal(err)
	}

	seedTestUser()
}

func seedTestUser() {
	roles := []string{"admin", "paciente", "psicologo"}
	for _, rol := range roles {
		_, err := db.Exec("INSERT OR IGNORE INTO rol (nombre) VALUES (?)", rol)
		if err != nil {
			log.Println("No se pudo insertar rol:", rol, err)
		}
	}

	var rolID int
	err := db.QueryRow("SELECT idrol FROM rol WHERE nombre = ?", "admin").Scan(&rolID)
	if err != nil {
		log.Println("No se encontró el rol admin:", err)
		return
	}

	hashed, _ := HashPassword("123456")
	_, err = db.Exec("INSERT OR IGNORE INTO usuario (username, password, rol_id) VALUES (?, ?, ?)", "adminuser", hashed, rolID)
	if err != nil {
		log.Println("No se pudo crear usuario de prueba:", err)
	}
}
