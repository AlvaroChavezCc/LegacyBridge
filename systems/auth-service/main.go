package main

import (
    "log"
    "net/http"

    "github.com/go-chi/chi/v5"
    "github.com/go-chi/chi/v5/middleware"
)

func main() {
    InitDB()

    r := chi.NewRouter()
    r.Use(middleware.Logger)

		r.Get("/health", func(w http.ResponseWriter, r *http.Request) {
			w.WriteHeader(http.StatusOK)
		})
    r.Post("/auth/login", LoginHandler)
    r.Get("/auth/verify", VerifyHandler)
    r.With(AuthMiddleware).Get("/auth/me", MeHandler)

    log.Println("Servidor escuchando en :8080")
    http.ListenAndServe(":8080", r)
}
