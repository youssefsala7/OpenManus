package main

import (
	"OpenManus/src/utils"
	"context"
	"fmt"

	"github.com/wailsapp/wails/v2/pkg/runtime"
)

// App struct
type App struct {
	ctx context.Context
}

type File struct {
	Result     string `json:"result"`
	Error      string `json:"error"`
	Callbackid string `json:"callbackid"`
}

// NewApp creates a new App application struct
func NewApp() *App {
	return &App{}
}

// startup is called when the app starts. The context is saved
// so we can call the runtime methods
func (a *App) startup(ctx context.Context) {
	a.ctx = ctx

	// 注册事件监听器
	runtime.EventsOn(ctx, "events", func(data ...interface{}) {
		if len(data) > 0 {
			for i := 0; i < len(data); i++ {
				fmt.Println("Received events with data:", data[i])
			}
		} else {
			fmt.Println("Received events without data")
		}
	})

	// 注册bat批处理事件监听器
	runtime.EventsOn(ctx, "bat", func(data ...interface{}) {
		if len(data) == 2 {
			fmt.Println("Received bat with data, batId: ", data[0])
			fmt.Println("Received bat with data, batPath: ", data[1])
			utils.ExecBatFile(a.ctx, data[0].(string), data[1].(string))
		} else if len(data) > 0 && len(data) < 2 {
			fmt.Println("Received bat with data, required 2 paramters, found 1: ", data[0])
		} else {
			fmt.Println("Received bat without data")
		}
	})

	// 注册执行py脚本监听器
	runtime.EventsOn(ctx, "pyFile", func(data ...interface{}) {
		if len(data) == 2 {
			fmt.Println("Received bat with data, batId: ", data[0])
			fmt.Println("Received bat with data, batPath: ", data[1])
			utils.ExecPyFile(a.ctx, data[0].(string), data[1].(string))
		} else if len(data) > 0 && len(data) < 2 {
			fmt.Println("Received bat with data, required 2 paramters, found 1: ", data[0])
		} else {
			fmt.Println("Received bat without data")
		}
	})

}

// Greet returns a greeting for the given name
func (a *App) Greet(name string) string {
	return fmt.Sprintf("Hello %s, It's show time!", name)
}

// ReadAll reads file content
func (a *App) ReadAll(filePath string) string {
	utils.Log("ReadAll filePath: ", filePath)
	// Read the file content, resulting in a JSON string containing file content and callback ID
	data := string(utils.ReadAll(filePath))
	utils.Log("ReadAll data: ", data)
	return data
}

func (a *App) SaveFile(filePath string, data string) {
	utils.SaveFile(filePath, data)
}

func (a *App) PathExists(path string) bool {
	exists, _ := utils.PathExists(path)
	return exists
}

func (a *App) DirSize(path string) int64 {
	utils.Log("DirSize path: ", path)
	size, _ := utils.DirSize(path)
	utils.Log("DirSize size: ", size)
	return size
}

func (a *App) AppPath() string {
	return utils.AppPath()
}
