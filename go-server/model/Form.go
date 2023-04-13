package model

import "time"

type HSB struct {
	H, S, B float32
}

type Form struct {
	Gender    string
	Age       int
	Name      string
	Colors    []HSB
	CreatedAt time.Time
}
