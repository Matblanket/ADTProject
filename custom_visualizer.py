# custom_visualizer.py
import math
import random
from typing import Dict, List, Set, Tuple

class CustomGraphVisualizer:
    
    def __init__(self):
        self.positions = {}
    
    def compute_spring_layout(self, vertices: List[int], edges: Set[Tuple[int, int]], 
                            iterations: int = 50) -> Dict[int, Tuple[float, float]]:
        positions = {}
        for v in vertices:
            positions[v] = (random.uniform(0, 1), random.uniform(0, 1))
        for _ in range(iterations):
            forces = {v: (0.0, 0.0) for v in vertices}
            for i, v1 in enumerate(vertices):
                for v2 in vertices[i+1:]:
                    dx = positions[v2][0] - positions[v1][0]
                    dy = positions[v2][1] - positions[v1][1]
                    distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
                    force = 0.1 / (distance * distance)
                    fx = force * dx / distance
                    fy = force * dy / distance
                    
                    forces[v1] = (forces[v1][0] - fx, forces[v1][1] - fy)
                    forces[v2] = (forces[v2][0] + fx, forces[v2][1] + fy)
            
            for u, v in edges:
                dx = positions[v][0] - positions[u][0]
                dy = positions[v][1] - positions[u][1]
                distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
                force = 0.01 * distance
                fx = force * dx / distance
                fy = force * dy / distance
                
                forces[u] = (forces[u][0] + fx, forces[u][1] + fy)
                forces[v] = (forces[v][0] - fx, forces[v][1] - fy)
            for v in vertices:
                x, y = positions[v]
                fx, fy = forces[v]
                positions[v] = (x + 0.1 * fx, y + 0.1 * fy)
        
        self._normalize_positions(positions, vertices)
        self.positions = positions
        return positions
    
    def _normalize_positions(self, positions: Dict[int, Tuple[float, float]], vertices: List[int]):
        if not positions:
            return
        
        xs = [pos[0] for pos in positions.values()]
        ys = [pos[1] for pos in positions.values()]
        
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        range_x = max_x - min_x if max_x != min_x else 1
        range_y = max_y - min_y if max_y != min_y else 1
        
        for v in vertices:
            x, y = positions[v]
            positions[v] = ((x - min_x) / range_x, (y - min_y) / range_y)
    
    def generate_ascii_art(self, vertices: List[int], edges: Set[Tuple[int, int]], 
                          coloring: Dict[int, int] = None, width: int = 60, height: int = 30) -> str:
        positions = self.compute_spring_layout(vertices, edges)
        grid = [[' ' for _ in range(width)] for _ in range(height)]
        scaled_positions = {}
        for v, (x, y) in positions.items():
            scaled_positions[v] = (int(x * (width-1)), int(y * (height-1)))
        for u, v in edges:
            x1, y1 = scaled_positions[u]
            x2, y2 = scaled_positions[v]
            self._draw_line(grid, x1, y1, x2, y2, '.')
        
        color_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for v, (x, y) in scaled_positions.items():
            if coloring and v in coloring:
                color_idx = coloring[v] - 1
                if color_idx < len(color_chars):
                    char = color_chars[color_idx]
                else:
                    char = 'X'  
            else:
                char = 'O'
            
            if 0 <= x < width and 0 <= y < height:
                grid[y][x] = char
        result = []
        for row in grid:
            result.append(''.join(row))
        return '\n'.join(result)
    
    def _draw_line(self, grid, x1, y1, x2, y2, char):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        while True:
            if 0 <= x1 < len(grid[0]) and 0 <= y1 < len(grid):
                grid[y1][x1] = char
            
            if x1 == x2 and y1 == y2:
                break
            
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy