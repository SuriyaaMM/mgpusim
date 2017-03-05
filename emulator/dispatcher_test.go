package emulator_test

import (
	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
	"gitlab.com/yaotsu/core/conn"
	"gitlab.com/yaotsu/gcn3/emulator"
)

type MockMapWorkGroupReqFactory struct {
	Reqs []*emulator.MapWorkGroupReq
}

func NewMockMapWorkGroupReqFactory() *MockMapWorkGroupReqFactory {
	return &MockMapWorkGroupReqFactory{make([]*emulator.MapWorkGroupReq, 0)}
}

func (f *MockMapWorkGroupReqFactory) Create() *emulator.MapWorkGroupReq {
	req := f.Reqs[0]
	f.Reqs = f.Reqs[1:]
	return req
}

var _ = Describe("Dispatcher", func() {
	var (
		dispatcher             *emulator.Dispatcher
		cu0                    *conn.MockComponent
		cu1                    *conn.MockComponent
		cu2                    *conn.MockComponent
		cu3                    *conn.MockComponent
		connection             *conn.DirectConnection
		mapWorkGroupReqFactory *MockMapWorkGroupReqFactory
	)

	BeforeEach(func() {
		mapWorkGroupReqFactory = NewMockMapWorkGroupReqFactory()
		dispatcher = emulator.NewDispatcher("dispatcher", mapWorkGroupReqFactory)
		cu0 = conn.NewMockComponent("cu0")
		cu0.AddPort("ToDispatcher")
		cu1 = conn.NewMockComponent("cu1")
		cu1.AddPort("ToDispatcher")
		cu2 = conn.NewMockComponent("cu2")
		cu2.AddPort("ToDispatcher")
		cu3 = conn.NewMockComponent("cu3")
		cu3.AddPort("ToDispatcher")
		connection = conn.NewDirectConnection()

		dispatcher.RegisterComputeUnit(cu0)
		dispatcher.RegisterComputeUnit(cu1)
		dispatcher.RegisterComputeUnit(cu2)
		dispatcher.RegisterComputeUnit(cu3)

		conn.PlugIn(dispatcher, "ToComputeUnits", connection)
		conn.PlugIn(cu0, "ToDispatcher", connection)
		conn.PlugIn(cu1, "ToDispatcher", connection)
		conn.PlugIn(cu2, "ToDispatcher", connection)
		conn.PlugIn(cu3, "ToDispatcher", connection)
	})

	It("should dispatch", func() {
		req := emulator.NewLaunchKernelReq()
		packet := new(emulator.HsaKernelDispatchPacket)
		packet.WorkgroupSizeX = 256
		packet.WorkgroupSizeY = 1
		packet.WorkgroupSizeZ = 1
		packet.GridSizeX = 1025
		packet.GridSizeY = 1
		packet.GridSizeZ = 1
		req.Packet = packet
		req.SetSendTime(0)

		mapReq0 := emulator.NewMapWorkGroupReq()
		mapReq1 := emulator.NewMapWorkGroupReq()
		mapReq2 := emulator.NewMapWorkGroupReq()
		mapReq3 := emulator.NewMapWorkGroupReq()
		mapWorkGroupReqFactory.Reqs = append(mapWorkGroupReqFactory.Reqs, mapReq0)
		mapWorkGroupReqFactory.Reqs = append(mapWorkGroupReqFactory.Reqs, mapReq1)
		mapWorkGroupReqFactory.Reqs = append(mapWorkGroupReqFactory.Reqs, mapReq2)
		mapWorkGroupReqFactory.Reqs = append(mapWorkGroupReqFactory.Reqs, mapReq3)

		cu0.ToReceiveReq(mapReq0, nil)
		cu1.ToReceiveReq(mapReq1, nil)
		cu2.ToReceiveReq(mapReq2, nil)
		cu3.ToReceiveReq(mapReq3, nil)

		dispatcher.Receive(req)

		Expect(cu0.AllReqReceived()).To(BeTrue())
		Expect(cu1.AllReqReceived()).To(BeTrue())
		Expect(cu2.AllReqReceived()).To(BeTrue())
		Expect(cu3.AllReqReceived()).To(BeTrue())

	})
})
