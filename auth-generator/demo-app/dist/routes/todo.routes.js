"use strict";
/**
 * Todo Routes
 * Example protected routes using generated auth
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.todoRouter = void 0;
const express_1 = require("express");
exports.todoRouter = (0, express_1.Router)();
const todos = [];
// Get all todos for current user
exports.todoRouter.get('/', (req, res) => {
    const userTodos = todos.filter(todo => todo.userId === req.user?.userId);
    res.json({
        todos: userTodos,
        count: userTodos.length
    });
});
// Create new todo
exports.todoRouter.post('/', (req, res) => {
    const { title } = req.body;
    if (!title || typeof title !== 'string') {
        return res.status(400).json({ error: 'Title is required' });
    }
    const todo = {
        id: Math.random().toString(36).substring(7),
        userId: req.user.userId,
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
exports.todoRouter.put('/:id', (req, res) => {
    const { id } = req.params;
    const { title, completed } = req.body;
    const todoIndex = todos.findIndex(t => t.id === id && t.userId === req.user.userId);
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
exports.todoRouter.delete('/:id', (req, res) => {
    const { id } = req.params;
    const todoIndex = todos.findIndex(t => t.id === id && t.userId === req.user.userId);
    if (todoIndex === -1) {
        return res.status(404).json({ error: 'Todo not found' });
    }
    todos.splice(todoIndex, 1);
    res.json({ message: 'Todo deleted' });
});
//# sourceMappingURL=todo.routes.js.map