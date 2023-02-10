package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"github.com/gagansingh894/mldeploy/pkg/pb/mldeploy"
	"log"
	"math/rand"
	"strconv"
	"sync"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {

	modelNamePtr := flag.String("model_name", "mymodel", "Specify the model to be used")
	numRecordsPtr := flag.Int("records", 300, " Number of records in a single request for which predictions are done")
	numIterPtr := flag.Int("iter", 500, " Number of iterations for benchmarking")
	flag.Parse()

	fmt.Println("creating client")
	conn, err := grpc.Dial("localhost:8000", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("failed to connect: %v", err)
	}

	defer conn.Close()
	tsClient := mldeploy.NewDeploymentServiceClient(conn)

	numRecords := *numRecordsPtr
	numIter := *numIterPtr

	if numRecords < 4 {
		log.Fatalf("failed to run benchmark. Minimum number of records required is 4")
	}

	fmt.Println("starting benchmark...")

	var wg sync.WaitGroup
	var records int

	fmt.Println("sending requests...")

	start := time.Now()
	for i := 0; i < numIter; i++ {
		rec := rand.Intn(numRecords) + 4

		wg.Add(1)
		go func() {
			req := createPredictionRequest(rec, 125, *modelNamePtr)
			makeSingleRequest(tsClient, req)
			records += rec
			wg.Done()
		}()
	}
	wg.Wait()
	totalTime := time.Since(start).Milliseconds()

	fmt.Println("average time taken:", totalTime/int64(numIter))
	fmt.Println("average records:", records/numIter)
}

func createPredictionRequest(numRecords, numFeatures int, modelName string) *mldeploy.PredictRequest {
	in := make(map[string][]float32)
	for i := 0; i < numFeatures; i++ {
		featureName := fmt.Sprintf("feature_%s", strconv.Itoa(i))
		data := make([]float32, numRecords)
		for j := 0; j < numRecords; j++ {
			data[j] = rand.Float32() * float32(rand.Intn(20))
		}
		in[featureName] = data
	}

	jsonStr, err := json.Marshal(in)
	if err != nil {
		panic("failed to marshal")
	}
	return &mldeploy.PredictRequest{
		ModelName: modelName,
		InputData: string(jsonStr),
	}
}

func makeSingleRequest(c mldeploy.DeploymentServiceClient, r *mldeploy.PredictRequest) {
	_, err := c.Predict(context.Background(), r)
	if err != nil {
		log.Fatalf("failed to call mldeploy service: %v", err)
	}
}
