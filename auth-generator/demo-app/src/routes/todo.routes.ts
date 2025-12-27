/**
 * Todo Routes
 * Example protected routes using generated auth
 */

import { Router, Request, Response } from 'express';

export const todoRouter = Router();

// In-memory todo storage (for demo purposes)
interface Todo {
  id: string;
  userId: string;
  title: string;
  completed: boolean;
  createdAt: Date;
}

const todos: Todo[] = [];

// Get all todos for current user
todoRouter.get('/', (req: Request, res: Response) => {
  const userTodos = todos.filter(todo => todo.userId === req.user?.userId);
  res.json({
    todos: userTodos,
    count: userTodos.length
  });
});

// Create new todo
todoRouter.post('/', (req: Request, res: Response) => {
  const { title } = req.body;

  if (!title || typeof title !== 'string') {
    return res.status(400).json({ error: 'Title is required' });
  }

  const todo: Todo = {
    id: Math.random().toString(36).substring(7),
    userId: req.user!.userId,
    title,
    completed: false,
    createdAt: new Date()
  };

  todos.push(todo);

  res.status(201).json({
    message: 'Todo created',
    todo
  });
});

// Update todo
todoRouter.put('/:id', (req: Request, res: Response) => {
  const { id } = req.params;
  const { title, completed } = req.body;

  const todoIndex = todos.findIndex(
    t => t.id === id && t.userId === req.user!.userId
  );

  if (todoIndex === -1) {
    return res.status(404).json({ error: 'Todo not found' });
  }

  if (title !== undefined) {
    todos[todoIndex].title = title;
  }

  if (completed !== undefined) {
    todos[todoIndex].completed = completed;
  }

  res.json({
    message: 'Todo updated',
    todo: todos[todoIndex]
  });
});

// Delete todo
todoRouter.delete('/:id', (req: Request, res: Response) => {
  const { id } = req.params;

  const todoIndex = todos.findIndex(
    t => t.id === id && t.userId === req.user!.userId
  );

  if (todoIndex === -1) {
    return res.status(404).json({ error: 'Todo not found' });
  }

  todos.splice(todoIndex, 1);

  res.json({ message: 'Todo deleted' });
});
