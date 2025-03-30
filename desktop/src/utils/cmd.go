package utils

import (
	"bufio"
	"context"
	"fmt"
	"os/exec"

	"github.com/wailsapp/wails/v2/pkg/runtime"
)

// ExecBat 执行bat文件
func ExecBatFile(ctx context.Context, batId string, batPath string) {
	Log("ExecBatFile batPath: ", batPath)
	if IsBlank(batId) || IsBlank(batPath) {
		fmt.Println("batId or batPath is nil")
		runtime.EventsEmit(ctx, batId, "error", "batId or batPath is nil")
		return
	}
	cmd := exec.Command("cmd", "/C", batPath)
	// 运行命令并获取输出
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		fmt.Println("Error creating StdoutPipe for Cmd:", err)
		runtime.EventsEmit(ctx, batId, "error", err.Error())
		return
	}
	stderr, err := cmd.StderrPipe()
	if err != nil {
		fmt.Println("Error creating StderrPipe for Cmd:", err)
		runtime.EventsEmit(ctx, batId, "error", err.Error())
		return
	}

	if err := cmd.Start(); err != nil {
		fmt.Println("Error starting cmd:", err)
		runtime.EventsEmit(ctx, batId, "error", err.Error())
		return
	}

	// 读取标准输出和错误输出
	outputScanner := bufio.NewScanner(stdout)
	errorScanner := bufio.NewScanner(stderr)

	go func() {
		for errorScanner.Scan() {
			// 处理错误输出
			fmt.Println("Error:", errorScanner.Text())
			runtime.EventsEmit(ctx, batId, "msg", errorScanner.Text())
		}
	}()

	for outputScanner.Scan() {
		// 处理标准输出
		fmt.Println("Output:", outputScanner.Text())
		// 在这里可以将输出逐行发送给客户端，例如通过HTTP响应写入等。
		runtime.EventsEmit(ctx, batId, "msg", outputScanner.Text())
	}

	if err := cmd.Wait(); err != nil {
		fmt.Println("Error waiting for cmd:", err)
		runtime.EventsEmit(ctx, batId, "error", err.Error())
	}
}
