#include <cpr/cpr.h>
#include <Eigen/Dense>
#include <chrono>
#include <iostream>
#include <nlohmann/json.hpp>

class Minion {
 private:
  Eigen::MatrixXd matrixCoefficients;
  Eigen::VectorXd vectorTerms;
  Eigen::VectorXd solutionVector;
  int uniqueId;
  bool isInitialized;

  // helper method to process JSON data
  void processJsonData(const nlohmann::json& jsonData) {
    uniqueId = jsonData["unique_id"];
    int size = jsonData["matrix_size"];
    matrixCoefficients.resize(size, size);
    vectorTerms.resize(size);

    for (int i = 0; i < size; ++i) {
      vectorTerms[i] = jsonData["vector"][i];
      for (int j = 0; j < size; ++j) {
        matrixCoefficients(i, j) = jsonData["matrix"][i][j];
      }
    }
  }

 public:
  Minion() : uniqueId(-1), isInitialized(false) {}

  // method to initialize the Minion with data from a server
  bool initialize(const std::string& url) {
    cpr::Response response = cpr::Get(cpr::Url{url});
    if (response.status_code != 200) {
      std::cerr << "Failed to retrieve data: " << response.status_code << std::endl;
      return false;
    }

    nlohmann::json jsonData = nlohmann::json::parse(response.text);
    processJsonData(jsonData);
    isInitialized = true;
    return true;
  }

  // method to solve the matrix equation
  void solve() {
    if (!isInitialized) {
      std::cerr << "Minion is not initialized!" << std::endl;
      return;
    }

    auto start = std::chrono::high_resolution_clock::now();
    // we wanted to optimize the computation using SVD with ComputeThinU and ComputeThinV because we know that C++ is already more performant than Python so we wanted to see to what extent we can still optimize
    solutionVector = matrixCoefficients.bdcSvd(Eigen::ComputeThinU | Eigen::ComputeThinV).solve(vectorTerms);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> elapsedTime = end - start;
    std::cout << "Minion [" << uniqueId << "] - Solution Time: " << elapsedTime.count() << " ms\n";
  }
};

int main() {
  Minion minion;
  if (minion.initialize("http://localhost:8000")) {
    minion.solve();
  }
  return 0;
}
