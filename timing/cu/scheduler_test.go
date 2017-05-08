package cu_test

import (
	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
	"gitlab.com/yaotsu/core"
	"gitlab.com/yaotsu/gcn3/insts"
	"gitlab.com/yaotsu/gcn3/kernels"
	"gitlab.com/yaotsu/gcn3/timing"
	"gitlab.com/yaotsu/gcn3/timing/cu"
)

func prepareGrid() *kernels.Grid {
	// Prepare a mock grid that is expanded
	grid := kernels.NewGrid()
	for i := 0; i < 5; i++ {
		wg := kernels.NewWorkGroup()
		grid.WorkGroups = append(grid.WorkGroups, wg)
		for j := 0; j < 10; j++ {
			wf := kernels.NewWavefront()
			wg.Wavefronts = append(wg.Wavefronts, wf)
		}
	}
	return grid
}

type MockWGMapper struct {
	OK bool
}

func (m *MockWGMapper) MapWG(req *timing.MapWGReq) bool {
	return m.OK
}

type MockWfDispatcher struct {
	OK bool
}

func (m *MockWfDispatcher) DispatchWf(evt *cu.DispatchWfEvent) bool {
	return m.OK
}

var _ = Describe("Scheduler", func() {
	var (
		scheduler    *cu.Scheduler
		connection   *core.MockConnection
		engine       *core.MockEngine
		wgMapper     *MockWGMapper
		wfDispatcher *MockWfDispatcher
		grid         *kernels.Grid
		status       *timing.KernelDispatchStatus
		co           *insts.HsaCo
	)

	BeforeEach(func() {
		engine = core.NewMockEngine()
		wgMapper = new(MockWGMapper)
		wfDispatcher = new(MockWfDispatcher)
		scheduler = cu.NewScheduler("scheduler", engine, wgMapper, wfDispatcher)
		scheduler.Freq = 1 * core.GHz
		connection = core.NewMockConnection()
		core.PlugIn(scheduler, "ToDispatcher", connection)

		grid = prepareGrid()
		status = timing.NewKernelDispatchStatus()
		status.Grid = grid
		co = insts.NewHsaCo()
		status.CodeObject = co
	})

	Context("when processing MapWGReq", func() {
		It("should process MapWGReq", func() {
			wg := kernels.NewWorkGroup()
			status := timing.NewKernelDispatchStatus()
			req := timing.NewMapWGReq(nil, scheduler, 10, wg, status)

			scheduler.Recv(req)

			Expect(engine.ScheduledEvent).NotTo(BeEmpty())
		})
	})

	Context("when processing DispatchWfReq", func() {
		It("should schedule DispatchWfEvent", func() {
			wg := grid.WorkGroups[0]
			wf := wg.Wavefronts[0]
			info := new(timing.WfDispatchInfo)
			req := timing.NewDispatchWfReq(nil, scheduler, 10, wf, info, 6256)

			scheduler.Recv(req)

			Expect(engine.ScheduledEvent).NotTo(BeEmpty())
		})
	})

	Context("when handling MapWGEvent", func() {
		It("should reply OK if wgMapper say OK", func() {
			req := timing.NewMapWGReq(nil, scheduler, 10, grid.WorkGroups[0],
				status)
			evt := cu.NewMapWGEvent(scheduler, 10, req)

			wgMapper.OK = true
			connection.ExpectSend(req, nil)

			scheduler.Handle(evt)

			Expect(connection.AllExpectedSent()).To(BeTrue())
			Expect(scheduler.RunningWGs).NotTo(BeEmpty())
			Expect(req.Ok).To(BeTrue())
		})

		It("should reply not OK if wgMapper say not OK", func() {
			req := timing.NewMapWGReq(nil, scheduler, 10, grid.WorkGroups[0],
				status)
			evt := cu.NewMapWGEvent(scheduler, 10, req)

			wgMapper.OK = false
			connection.ExpectSend(req, nil)

			scheduler.Handle(evt)

			Expect(connection.AllExpectedSent()).To(BeTrue())
			Expect(req.Ok).To(BeFalse())
		})

	})

	Context("when handling dispatch wavefront request", func() {
		It("should reschedule DispatchWfEvent if not complete", func() {
			wf := grid.WorkGroups[0].Wavefronts[0]
			info := new(timing.WfDispatchInfo)
			info.SIMDID = 1
			req := timing.NewDispatchWfReq(nil, scheduler, 10, wf, info, 6256)
			evt := cu.NewDispatchWfEvent(scheduler, 10, req)

			wfDispatcher.OK = false
			scheduler.Handle(evt)

			Expect(len(engine.ScheduledEvent)).To(Equal(1))
		})
	})
})
