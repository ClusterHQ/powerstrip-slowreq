package main

import (
	"encoding/json"
	"flag"
	_ "fmt"
	_ "io/ioutil"
	"log"
	"net/http"
	"os"
	"time"
)

var delay = flag.Duration("d", 1*time.Second, "duration to delay. default: 1s")

func main() {
	flag.Parse()

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		defer r.Body.Close()
		d := json.NewDecoder(r.Body)
		var request map[string]interface{}
		if err := d.Decode(&request); err != nil {
			http.Error(w, "bad request", 400)
			return
		}
		time.Sleep(*delay)
		response := make(map[string]interface{})
		response["PowerstripProtocolVersion"] = 1
		if request["Type"] == "pre-hook" {
			response["ModifiedClientRequest"] = request["ClientRequest"]
		} else if request["Type"] == "post-hook" {
			response["ModifiedServerResponse"] = request["ServerResponse"]
		} else {
			http.Error(w, "bad request", 400)
			return
		}
		bytes, err := json.MarshalIndent(response, "", "  ")
		if err != nil {
			http.Error(w, "failed marshal", 500)
			log.Println("error:", err)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write(bytes)
	})
	log.Println("serving on", os.Getenv("PORT"), "with", (*delay).String(), "...")
	log.Fatal(http.ListenAndServe(":"+os.Getenv("PORT"), nil))
}
