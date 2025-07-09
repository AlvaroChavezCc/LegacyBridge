package main

import (
	"database/sql"
	"encoding/json"
	"log"
	"net/http"
)

func LoginHandler(w http.ResponseWriter, r *http.Request) {
	var req LoginRequest
	json.NewDecoder(r.Body).Decode(&req)

	row := db.QueryRow(`
		SELECT u.password, r.nombre 
		FROM usuario u
		JOIN rol r ON u.rol_id = r.idrol
		WHERE u.username = ?`, req.Username)

	var hashed, role string
	err := row.Scan(&hashed, &role)
	if err == sql.ErrNoRows || !CheckPassword(hashed, req.Password) {
		http.Error(w, "Credenciales inválidas", http.StatusUnauthorized)
		return
	}

	token, _ := GenerateJWT(req.Username, role)
	json.NewEncoder(w).Encode(map[string]string{
		"token": token,
		"rol":   role,
	})
}

func VerifyHandler(w http.ResponseWriter, r *http.Request) {
	tokenStr := r.Header.Get("Authorization")
	username, err := ParseJWT(tokenStr)
	if err != nil {
		http.Error(w, "Token inválido", http.StatusUnauthorized)
		return
	}
	json.NewEncoder(w).Encode(map[string]string{"username": username})
}

func MeHandler(w http.ResponseWriter, r *http.Request) {
	username := r.Context().Value("username")

	strUsername, ok := username.(string)
	if !ok || strUsername == "" {
		http.Error(w, "Username no válido en el contexto", http.StatusUnauthorized)
		return
	}

	row := db.QueryRow("SELECT idusuario, username FROM usuario WHERE username = ?", strUsername)
	var user User
	err := row.Scan(&user.ID, &user.Username)
	if err != nil {
		log.Println("No se encontró el usuario:", err)
		http.Error(w, "Usuario no encontrado", http.StatusNotFound)
		return
	}

	json.NewEncoder(w).Encode(user)
}
