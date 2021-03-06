import FWCore.ParameterSet.Config as cms

def customiseCommon(process):
    
    #####################################################################################################
    ####
    ####  Top level replaces for handling strange scenarios of early collisions
    ####

    ## TRACKING:
    process.newSeedFromTriplets.OrderedHitsFactoryPSet.GeneratorPSet.maxElement = cms.uint32(100000)
    process.newSeedFromPairs.OrderedHitsFactoryPSet.maxElement = cms.uint32(100000)
    process.secTriplets.OrderedHitsFactoryPSet.GeneratorPSet.maxElement = cms.uint32(100000)
    process.thTripletsA.OrderedHitsFactoryPSet.GeneratorPSet.maxElement = cms.uint32(100000)
    process.thTripletsB.OrderedHitsFactoryPSet.GeneratorPSet.maxElement = cms.uint32(100000)
    process.fourthPLSeeds.OrderedHitsFactoryPSet.maxElement = cms.uint32(100000)
    process.fifthSeeds.OrderedHitsFactoryPSet.maxElement = cms.uint32(100000)
    
    ###### FIXES TRIPLETS FOR LARGE BS DISPLACEMENT ######

    ### prevent bias in pixel vertex
    process.pixelVertices.useBeamConstraint = False
    
    ###
    ###  end of top level replacements
    ###
    ###############################################################################################

    return (process)


##############################################################################
def customisePPData(process):
    process= customiseCommon(process)

    ## particle flow HF cleaning
    process.particleFlowRecHitHCAL.LongShortFibre_Cut = 30.
    process.particleFlowRecHitHCAL.ApplyPulseDPG = True

    ## HF cleaning for data only
    process.hcalRecAlgos.SeverityLevels[3].RecHitFlags.remove("HFDigiTime")
    process.hcalRecAlgos.SeverityLevels[4].RecHitFlags.append("HFDigiTime")

    ##beam-halo-id for data only
    process.CSCHaloData.ExpectedBX = cms.int32(3)

    ## hcal hit flagging
    process.hfreco.PETstat.flagsToSkip  = 2
    process.hfreco.S8S1stat.flagsToSkip = 18
    process.hfreco.S9S1stat.flagsToSkip = 26
    
    return process


##############################################################################
def customisePPMC(process):
    process=customiseCommon(process)
    
    return process

##############################################################################
def customiseCosmicData(process):

    return process

##############################################################################
def customiseCosmicMC(process):
    
    return process
        
##############################################################################
def customiseVALSKIM(process):
    process= customisePPData(process)
    process.reconstruction.remove(process.lumiProducer)
    return process
                
##############################################################################
def customiseExpress(process):
    process= customisePPData(process)

    import RecoVertex.BeamSpotProducer.BeamSpotOnline_cfi
    process.offlineBeamSpot = RecoVertex.BeamSpotProducer.BeamSpotOnline_cfi.onlineBeamSpotProducer.clone()
    
    return process

##############################################################################
def customisePrompt(process):
    process= customisePPData(process)

    import RecoVertex.BeamSpotProducer.BeamSpotOnline_cfi
    process.offlineBeamSpot = RecoVertex.BeamSpotProducer.BeamSpotOnline_cfi.onlineBeamSpotProducer.clone()
    
    return process

##############################################################################
##############################################################################

def customiseCommonHI(process):
    
    ###############################################################################################
    ####
    ####  Top level replaces for handling strange scenarios of early HI collisions
    ####

    ## Offline Silicon Tracker Zero Suppression
    process.siStripZeroSuppression.Algorithms.PedestalSubtractionFedMode = cms.bool(False)
    process.siStripZeroSuppression.Algorithms.CommonModeNoiseSubtractionMode = cms.string("IteratedMedian")
    process.siStripZeroSuppression.doAPVRestore = cms.bool(True)
    process.siStripZeroSuppression.storeCM = cms.bool(True)

    ## Fixes to protect against large BS displacements
    process.hiPixel3ProtoTracks.RegionFactoryPSet.RegionPSet.originRadius = 0.2
    process.hiPixel3ProtoTracks.RegionFactoryPSet.RegionPSet.fixedError = 0.5
    process.hiSelectedProtoTracks.maxD0Significance = 100
    process.hiPixelAdaptiveVertex.TkFilterParameters.maxD0Significance = 100
    process.hiPixelAdaptiveVertex.useBeamConstraint = False
    process.hiPixelAdaptiveVertex.PVSelParameters.maxDistanceToBeam = 1.0

    ###
    ###  end of top level replacements
    ###
    ###############################################################################################

    return process

##############################################################################
def customiseExpressHI(process):
    process= customiseCommonHI(process)

    import RecoVertex.BeamSpotProducer.BeamSpotOnline_cfi
    process.offlineBeamSpot = RecoVertex.BeamSpotProducer.BeamSpotOnline_cfi.onlineBeamSpotProducer.clone()

    # keep some debugging content for zero suppression
    process.siStripZeroSuppression.produceRawDigis = cms.bool(True)
    process.siStripZeroSuppression.produceCalculatedBaseline = cms.bool(True)
    
    return process

##############################################################################
def customisePromptHI(process):
    process= customiseCommonHI(process)

    import RecoVertex.BeamSpotProducer.BeamSpotOnline_cfi
    process.offlineBeamSpot = RecoVertex.BeamSpotProducer.BeamSpotOnline_cfi.onlineBeamSpotProducer.clone()
    
    return process

##############################################################################
def customiseAlcaOnlyPromptHI(process):
    process= customiseCommonHI(process)

    import RecoVertex.BeamSpotProducer.BeamSpotOnline_cfi
    process.offlineBeamSpot = RecoVertex.BeamSpotProducer.BeamSpotOnline_cfi.onlineBeamSpotProducer.clone()

    import HLTrigger.HLTfilters.hltHighLevel_cfi
    process.hltCentralityVeto = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
        HLTPaths = cms.vstring('HLT_HICentralityVeto'),
        throw = cms.bool(False)
    )

    for path in process.paths:
        getattr(process,path)._seq = process.hltCentralityVeto * getattr(process,path)._seq
    
    return process

##############################################################################
