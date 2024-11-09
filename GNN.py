np.math = math
from torch_geometric.nn import radius_graph
from torch_geometric.nn.models.dimenet import (
    BesselBasisLayer,
    EmbeddingBlock,
    ResidualLayer,
    SphericalBasisLayer,
    OutputBlock,
    InteractionPPBlock,
    InteractionBlock,
    triplets
)
import torch.nn as nn
import torch
class GNN():
    def __init__(self,cutoff=8.0,max_num_neighbors=32,num_radial=16,envelope_exponent=5,num_spherical=6):
        self.cutoff = cutoff
        self.max_num_neighbors = max_num_neighbors
        self.rbf = BesselBasisLayer(num_radial, cutoff, envelope_exponent)
        self.sbf = SphericalBasisLayer(num_spherical, num_radial, cutoff,
                                       envelope_exponent)

    def DimnetPlusLocalEnvironment(self,z,pos,batch=None):
        edge_index = radius_graph(pos, r=self.cutoff, batch=batch,
                                  max_num_neighbors=self.max_num_neighbors)

        i, j, idx_i, idx_j, idx_k, idx_kj, idx_ji = triplets(
            edge_index, num_nodes=z)

        # Calculate distances.
        dist = (pos[i] - pos[j]).pow(2).sum(dim=-1).sqrt()

        pos_jk, pos_ij = pos[idx_j] - pos[idx_k], pos[idx_i] - pos[idx_j]
        a = (pos_ij * pos_jk).sum(dim=-1)
        b = torch.cross(pos_ij, pos_jk).norm(dim=-1)
        angle = torch.atan2(b, a)
        rbf = self.rbf(dist)
        sbf = self.sbf(dist, angle, idx_kj)
        return rbf,sbf






    
