package model

import "time"

type HSB struct {
	H, S, V float32
}

type Form struct {
	Zjuid     string
	Name      string
	Colors    []HSB
	CreatedAt time.Time
}
