package l1v

import (
	"gitlab.com/akita/akita"
	"gitlab.com/akita/mem"
	"gitlab.com/akita/util"
)

type bankStage struct {
	inBuf   util.Buffer
	storage *mem.Storage
	latency int

	cycleLeft int
	currTrans *transaction
}

func (s *bankStage) Tick(now akita.VTimeInSec) bool {
	if s.currTrans != nil {
		s.cycleLeft--

		if s.cycleLeft < 0 {
			return s.finalizeTrans(now)
		}

		return true
	}
	return s.extractFromBuf()
}

func (s *bankStage) extractFromBuf() bool {
	item := s.inBuf.Peek()
	if item == nil {
		return false
	}

	s.currTrans = item.(*transaction)
	s.cycleLeft = s.latency
	s.inBuf.Pop()
	return true
}

func (s *bankStage) finalizeTrans(now akita.VTimeInSec) bool {
	switch s.currTrans.bankAction {
	case bankActionReadHit:
		return s.finalizeReadHitTrans(now)
	case bankActionWrite:
		return s.finalizeWriteTrans(now)
	case bankActionWriteFetched:
		return s.finalizeWriteFetchedTrans(now)
	default:
		panic("cannot handle trans bank action")
	}
}

func (s *bankStage) finalizeReadHitTrans(now akita.VTimeInSec) bool {
	trans := s.currTrans
	block := trans.block

	data, err := s.storage.Read(block.CacheAddress, trans.read.MemByteSize)
	if err != nil {
		panic(err)
	}
	block.ReadCount--

	for _, t := range trans.preCoalesceTransactions {
		offset := t.read.Address - block.Tag
		t.data = data[offset : offset+t.read.MemByteSize]
		t.done = true
	}

	s.currTrans = nil
	return true
}

func (s *bankStage) finalizeWriteTrans(now akita.VTimeInSec) bool {
	trans := s.currTrans
	block := trans.block

	err := s.storage.Write(block.CacheAddress, trans.write.Data)
	if err != nil {
		panic(err)
	}
	block.DirtyMask = trans.write.DirtyMask
	block.IsLocked = false

	s.currTrans = nil
	return true
}

func (s *bankStage) finalizeWriteFetchedTrans(now akita.VTimeInSec) bool {
	trans := s.currTrans
	block := trans.block

	err := s.storage.Write(block.CacheAddress, trans.data)
	if err != nil {
		panic(err)
	}

	block.DirtyMask = trans.writeFetchedDirtyMask
	block.IsLocked = false

	s.currTrans = nil
	return true
}
