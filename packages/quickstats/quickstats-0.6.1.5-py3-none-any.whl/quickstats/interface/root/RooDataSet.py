import ROOT

from quickstats.interface.cppyy.vectorize import as_np_array

class RooDataSet:
    @staticmethod
    def extract_category_data(dataset:ROOT.RooDataSet, observables:ROOT.RooArgSet, category:ROOT.RooCategory):
        result = ROOT.RFUtils.ExtractCategoryData(dataset, observables, category)
        
        obs_values = as_np_array(result.observable_values)
        n_entries = dataset.numEntries()
        category_data = {}
        for i, obs in enumerate(observables):
            obs_name = obs.GetName()
            category_data[obs_name] = obs_values[i*n_entries: (i + 1)*n_entries]
        category_data['weight'] = as_np_array(result.weights)
        category_data['label'] = as_np_array(result.category_labels)
        category_data['index'] = as_np_array(result.category_index)
        return category_data