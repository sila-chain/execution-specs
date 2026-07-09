package main

import (
	"encoding/json"
	"io/ioutil"

	"github.com/sila/go-sila/core"
)

func main() {
	genesis := core.DefaultGenesisBlock()

	file, _ := json.MarshalIndent(genesis, "", "    ")
	_ = ioutil.WriteFile("genesis.json", file, 0644)
}
