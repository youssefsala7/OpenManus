package utils

import (
	"fmt"
	"io"
	"os"
	"path/filepath"
)

// ReadAll file content
func ReadAll(filePath string) []byte {
	if IsBlank(filePath) {
		fmt.Println("File path is nil")
		return nil
	}
	file, err := os.Open(filePath)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return nil
	}
	// 确保文件最后被关闭
	defer file.Close()

	data, err := io.ReadAll(file)
	if err != nil {
		fmt.Println("Read file error:", err)
		return nil
	}
	return data
}

// SaveFile
func SaveFile(filePath string, data string) {
	if IsBlank(filePath) {
		fmt.Println("File path is nil")
		return
	}
	file, err := os.Create(filePath)
	if err != nil {
		fmt.Println("Error create file:", err)
		return
	}
	// 确保文件最后被关闭
	defer file.Close()

	_, err = file.WriteString(data)
	if err != nil {
		fmt.Println("Write file error:", err)
		return
	}
	return
}

func PathExists(path string) (bool, error) {
	_, err := os.Stat(path)
	// 文件或目录已经存在
	if err == nil {
		return true, nil
	}
	if os.IsNotExist(err) {
		return false, nil
	}
	return false, err
}

func DirSize(path string) (int64, error) {
	var size int64
	err := filepath.Walk(path, func(_ string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if !info.IsDir() {
			size += info.Size()
		}
		return nil
	})
	return size, err
}

func AppPath() string {
	exePath, err := os.Executable()
	if err != nil {
		panic(err)
	}
	appDir := filepath.Dir(exePath)
	fmt.Println("Application Directory:", appDir)
	return appDir
}
