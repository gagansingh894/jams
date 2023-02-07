package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"github.com/gagansingh894/treeserve/pkg/pb/treeserve"
	"log"
	"math"
	"math/rand"
	"strconv"
	"time"

	"golang.org/x/sync/errgroup"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {

	modelNamePtr := flag.String("model_name", "mymodel", "Specify the model to be used")
	isParallelPtr := flag.Bool("parallel", false, " Determine whether to parallelize request")
	numRecordsPtr := flag.Int("records", 300, " Number of records in a single request for which predictions are done")
	numIterPtr := flag.Int("iter", 500, " Number of iterations for benchmarking")
	flag.Parse()

	fmt.Println("creating client")
	conn, err := grpc.Dial("localhost:8000", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("failed to connect: %v", err)
	}

	defer conn.Close()
	tsClient := treeserve.NewDeploymentServiceClient(conn)

	var (
		records   int
		totalTime int64
	)

	numRecords := *numRecordsPtr
	numIter := *numIterPtr

	if numRecords < 4 {
		log.Fatalf("failed to run benchmark. Minimum number of records required is 4")
	}

	fmt.Println("sending requests...")
	if *isParallelPtr {
		fmt.Println("benchmarking using parallel mode")
	} else {
		fmt.Println("benchmarking using single mode")
	}

	for i := 0; i < numIter; i++ {
		start := time.Now()

		if *isParallelPtr {
			req := divideAndCreatePredictionRequest(rand.Intn(numRecords)+4, 4, *modelNamePtr)
			makeParallelRequests(tsClient, req)
		} else {
			req := createPredictionRequest(rand.Intn(numRecords)+4, 125, *modelNamePtr)
			makeSingleRequests(tsClient, req)
		}

		elapsed := time.Since(start)

		records += *numRecordsPtr
		totalTime += elapsed.Milliseconds()
	}

	fmt.Println("average time taken:", totalTime/int64(numIter))
	fmt.Println("average records:", records/numIter)
}

func divideAndCreatePredictionRequest(numRecords, n int, modelName string) []*treeserve.PredictRequest {
	s := int(math.Ceil(float64(numRecords / n)))
	out := make([]*treeserve.PredictRequest, n)

	t := numRecords
	for i := 0; i < n; i++ {
		out[i] = createPredictionRequest(t, 125, modelName)
		t -= s
		if t < s {
			s = t
		}
	}
	return out
}

func createPredictionRequest(numRecords, numFeatures int, modelName string) *treeserve.PredictRequest {
	in := make(map[string][]float32)
	for i := 0; i <= numFeatures; i++ {
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
	return &treeserve.PredictRequest{
		ModelName: modelName,
		InputData: string(jsonStr),
	}
}

func makeSingleRequests(c treeserve.DeploymentServiceClient, r *treeserve.PredictRequest) {
	_, err := c.Predict(context.Background(), r)
	if err != nil {
		log.Fatalf("failed to call Treeserve service: %v", err)
	}
}

func makeParallelRequests(c treeserve.DeploymentServiceClient, r []*treeserve.PredictRequest) {
	numPartitions := 4
	out := make([]*treeserve.PredictResponse, numPartitions)
	g, ctx := errgroup.WithContext(context.Background())
	for j := 0; j < numPartitions; j++ {
		partitionNum := j
		g.Go(func() error {
			pred, err := c.Predict(ctx, r[partitionNum])
			if err != nil {
				log.Fatalf("failed to call Treeserve service: %v", err)
			}
			out[partitionNum] = pred
			return nil
		})
	}
	err := g.Wait()
	if err != nil {
		log.Fatalf("failed to get predictions: %s", err)
	}

	_ = combinePredictions(out)
}

func combinePredictions(in []*treeserve.PredictResponse) []float64 {
	var out []float64
	for _, predResponse := range in {
		for _, pred := range predResponse.Predictions {
			out = append(out, pred)
		}
	}
	return out
}
