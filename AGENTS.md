# Research Paper Agent - arXiv Paper Aggregator

A modern full-stack task management application built with React, Node.js, and PostgreSQL. Users can create projects, manage tasks, collaborate with team members, and track progress in real-time.

**Tech Stack**: React 18 + TypeScript, Node.js + Express, PostgreSQL, Prisma ORM, TailwindCSS, Vite

---

## Core Commands

### Development
- Install dependencies: `npm install`
- Start dev server (frontend): `npm run dev`
- Start backend server: `npm run server:dev`
- Start both concurrently: `npm run dev:full`
- Type-check: `npm run type-check`
- Lint code: `npm run lint`
- Auto-fix lint issues: `npm run lint:fix`
- Format code: `npm run format`

### Testing
- Run all tests: `npm test`
- Run tests in watch mode: `npm run test:watch`
- Run specific test file: `npm test -- src/components/TaskCard.test.tsx`
- Run tests with coverage: `npm run test:coverage`
- Run E2E tests: `npm run test:e2e`

### Database
- Run migrations: `npm run db:migrate`
- Generate Prisma client: `npm run db:generate`
- Seed database: `npm run db:seed`
- Open Prisma Studio: `npm run db:studio`
- Reset database: `npm run db:reset`

### Build & Deploy
- Build for production: `npm run build`
- Preview production build: `npm run preview`
- Build backend: `npm run build:server`
- Start production server: `npm run start`

---

## Development Environment Setup

### Prerequisites
- Node.js >= 18.0.0
- PostgreSQL >= 14.0
- npm >= 9.0.0

### Initial Setup
1. Clone repository and install dependencies: `npm install`
2. Copy environment file: `cp .env.example .env`
3. Configure `.env` with your database credentials and API keys
4. Run database migrations: `npm run db:migrate`
5. Seed initial data: `npm run db:seed`
6. Start development servers: `npm run dev:full`

### Environment Variables Required
```
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/taskflow"

# Authentication
JWT_SECRET="your-secret-key-min-32-chars"
JWT_EXPIRES_IN="7d"

# Frontend
VITE_API_URL="http://localhost:3000/api"
VITE_WS_URL="ws://localhost:3000"

# Email (optional)
SMTP_HOST="smtp.gmail.com"
SMTP_PORT="587"
SMTP_USER="your-email@gmail.com"
SMTP_PASS="your-app-password"

# Storage (optional)
AWS_S3_BUCKET="taskflow-uploads"
AWS_ACCESS_KEY_ID="your-access-key"
AWS_SECRET_ACCESS_KEY="your-secret-key"
```

### IDE Configuration
- VSCode recommended extensions: ESLint, Prettier, Prisma, Tailwind CSS IntelliSense
- Enable format on save in VSCode settings
- Use the provided `.vscode/settings.json` for consistent formatting

---

## Testing Instructions

### Test Organization
- Unit tests: `src/**/*.test.tsx` or `src/**/*.test.ts`
- Integration tests: `tests/integration/**/*.test.ts`
- E2E tests: `tests/e2e/**/*.spec.ts`
- Test utilities: `tests/utils/` and `tests/fixtures/`

### Testing Guidelines
- All new features must include unit tests
- API endpoints require integration tests
- Critical user flows need E2E tests
- Minimum 80% code coverage for new code
- Use `describe` blocks to group related tests
- Use `it` or `test` for individual test cases
- Mock external services and API calls

### Running Specific Tests
```bash
# Run tests for a component
npm test -- TaskCard

# Run tests matching a pattern
npm test -- --testNamePattern="should create task"

# Run tests in a specific folder
npm test -- tests/integration

# Update snapshots
npm test -- -u
```

### CI/CD Pipeline
- GitHub Actions workflow in `.github/workflows/ci.yml`
- Runs on all PRs and pushes to main
- Steps: install → lint → type-check → test → build
- All checks must pass before merge

---

## Architecture Overview

### Project Structure
```
taskflow/
├── src/
│   ├── components/          # React components
│   │   ├── common/          # Reusable UI components
│   │   ├── tasks/           # Task-related components
│   │   ├── projects/        # Project-related components
│   │   └── layouts/         # Page layouts
│   ├── pages/               # Route pages
│   ├── hooks/               # Custom React hooks
│   ├── services/            # API service layer
│   ├── store/               # State management (Zustand)
│   ├── types/               # TypeScript type definitions
│   ├── utils/               # Utility functions
│   └── styles/              # Global styles and Tailwind config
├── server/
│   ├── controllers/         # Request handlers
│   ├── middleware/          # Express middleware
│   ├── models/              # Business logic
│   ├── routes/              # API routes
│   ├── services/            # External service integrations
│   ├── utils/               # Server utilities
│   └── validators/          # Request validation schemas
├── prisma/
│   ├── schema.prisma        # Database schema
│   ├── migrations/          # Database migrations
│   └── seed.ts              # Seed data
└── tests/                   # Test files
```

### Key Design Patterns
- **Component Pattern**: Atomic design - atoms, molecules, organisms
- **State Management**: Zustand stores with TypeScript for type safety
- **API Layer**: Service classes that wrap fetch calls
- **Backend**: MVC pattern with controllers, models, and routes separated
- **Database**: Prisma ORM with repository pattern
- **Authentication**: JWT-based with refresh token rotation
- **Real-time**: WebSocket connections for live updates

### Data Flow
1. User interacts with React component
2. Component dispatches action to Zustand store
3. Store calls API service method
4. Service makes HTTP request to backend
5. Backend controller validates request
6. Controller calls model/service for business logic
7. Prisma queries database
8. Response flows back through layers
9. Store updates, triggering component re-render

---

## Code Conventions & Patterns

### Naming Conventions
- **Components**: PascalCase (e.g., `TaskCard.tsx`, `ProjectList.tsx`)
- **Hooks**: camelCase with "use" prefix (e.g., `useAuth.ts`, `useTasks.ts`)
- **Utils/Services**: camelCase (e.g., `formatDate.ts`, `taskService.ts`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `API_ENDPOINTS`, `MAX_FILE_SIZE`)
- **Types/Interfaces**: PascalCase with "I" prefix for interfaces (e.g., `ITask`, `IUser`)
- **Folders**: kebab-case (e.g., `task-details`, `user-profile`)

### File Organization
- One component per file
- Co-locate tests with source files (e.g., `TaskCard.tsx` and `TaskCard.test.tsx`)
- Index files for clean imports: `components/tasks/index.ts`
- Group related files in feature folders

### Import Order
```typescript
// 1. External dependencies
import React from 'react';
import { useNavigate } from 'react-router-dom';

// 2. Internal absolute imports
import { Button } from '@/components/common';
import { useAuth } from '@/hooks';
import { taskService } from '@/services';

// 3. Types
import type { ITask } from '@/types';

// 4. Relative imports
import { TaskCard } from './TaskCard';

// 5. Styles
import './styles.css';
```

### Code Style
- Use TypeScript for all new code - no `any` types
- Use functional components with hooks, not class components
- Prefer `const` over `let`, avoid `var`
- Use arrow functions for callbacks
- Destructure props and state
- Use template literals over string concatenation
- Keep functions small and single-purpose (max 50 lines)
- Use early returns to reduce nesting
- Add JSDoc comments for complex functions
- Use explicit return types for functions

### Component Patterns
```typescript
// Preferred component structure
interface TaskCardProps {
  task: ITask;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
}

export const TaskCard: React.FC<TaskCardProps> = ({ task, onEdit, onDelete }) => {
  // Hooks at the top
  const { user } = useAuth();
  const navigate = useNavigate();
  
  // Event handlers
  const handleEdit = () => {
    onEdit(task.id);
  };
  
  // Early returns for conditional rendering
  if (!task) return null;
  
  // Main render
  return (
    <div className="task-card">
      {/* Component JSX */}
    </div>
  );
};
```

### API Response Format
All API responses follow this structure:
```typescript
{
  success: boolean;
  data?: T;
  error?: {
    message: string;
    code: string;
    details?: unknown;
  };
  meta?: {
    page?: number;
    limit?: number;
    total?: number;
  };
}
```

### Error Handling
- Use try-catch blocks for async operations
- Display user-friendly error messages
- Log errors to console in development
- Send errors to logging service in production
- Use error boundaries for React component errors

---

## Git Workflow

### Branch Naming
- Feature branches: `feature/task-filters`
- Bug fixes: `fix/login-validation`
- Hotfixes: `hotfix/critical-bug`
- Refactoring: `refactor/api-service`
- Documentation: `docs/update-readme`

### Commit Message Format
Follow conventional commits:
```
type(scope): subject

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`

Examples:
- `feat(tasks): add task filtering by status`
- `fix(auth): resolve token expiration issue`
- `docs(readme): update installation instructions`
- `test(tasks): add unit tests for TaskCard component`

### Pull Request Requirements
- **Title format**: `[Feature/Fix] Brief description`
- **Description must include**:
  - What changes were made
  - Why the changes were necessary
  - How to test the changes
  - Screenshots for UI changes
  - Link to related issue
- **Before submitting**:
  - Run `npm run lint` and fix all issues
  - Run `npm run type-check` and resolve all errors
  - Run `npm test` and ensure all tests pass
  - Update documentation if needed
  - Self-review your code
  - Test your changes locally
- **Review requirements**:
  - At least 1 approval required
  - All CI checks must pass
  - No merge conflicts

### Pre-commit Hooks
Husky runs these checks before each commit:
- Lint staged files
- Type-check TypeScript
- Run tests related to changed files
- Format code with Prettier

If any check fails, the commit is blocked.

---

## Security Considerations

### Authentication & Authorization
- All API routes (except login/register) require JWT authentication
- JWTs stored in httpOnly cookies, not localStorage
- Implement refresh token rotation
- Passwords hashed with bcrypt (minimum 12 rounds)
- Rate limiting on auth endpoints (max 5 attempts per 15 minutes)
- Validate user permissions before data operations

### Data Protection
- Sanitize all user inputs to prevent XSS
- Use parameterized queries (Prisma handles this)
- Implement CSRF protection for state-changing operations
- Validate and sanitize file uploads
- Set appropriate CORS headers
- Use helmet.js for security headers

### Secrets Management
- **NEVER commit** `.env` files, API keys, or credentials
- Use environment variables for all sensitive data
- Rotate secrets regularly
- Use different secrets for dev/staging/production
- Store production secrets in secure vault (AWS Secrets Manager, etc.)

### API Security
- Implement rate limiting (100 requests per 15 minutes per IP)
- Validate all request bodies with Zod schemas
- Return generic error messages (don't leak system info)
- Log security events (failed logins, invalid tokens)
- Use HTTPS in production only

### Common Security Gotchas
- Don't send passwords in API responses
- Don't expose user emails publicly
- Don't trust client-side validation alone
- Don't use predictable IDs (use UUIDs)
- Don't log sensitive data

---

## Dependencies & Package Management

### Adding New Dependencies
```bash
# Add to project dependencies
npm install package-name

# Add to dev dependencies
npm install -D package-name

# Add to specific workspace
npm install package-name --workspace=server
```

### Dependency Guidelines
- Check package weekly downloads and maintenance status
- Prefer well-maintained packages with recent updates
- Avoid packages with known security vulnerabilities
- Keep dependencies up to date but test before upgrading
- Document why specific packages were chosen

### Version Constraints
- Use exact versions for critical dependencies: `"5.2.1"`
- Use caret for most packages: `"^5.2.0"` (allows patches and minors)
- Use tilde for conservative updates: `"~5.2.0"` (allows patches only)
- Lock file (`package-lock.json`) must be committed

### Updating Dependencies
```bash
# Check for outdated packages
npm outdated

# Update all packages (respecting semver)
npm update

# Update to latest (including major versions)
npm install package-name@latest

# After updating, always test thoroughly
npm run lint && npm run type-check && npm test
```

---

## Domain-Specific Vocabulary

### Business Terms
- **Project**: A container for tasks, has members and settings
- **Task**: A unit of work with title, description, status, assignee
- **Sprint**: Time-boxed iteration containing tasks (1-4 weeks)
- **Board**: Kanban-style view of tasks organized by status
- **Workspace**: Top-level organization containing projects
- **Member**: User with specific role (owner, admin, member, viewer)

### Status Definitions
- **Backlog**: Task created but not yet planned
- **Todo**: Task planned for current sprint
- **In Progress**: Task actively being worked on
- **In Review**: Task completed, awaiting review
- **Done**: Task completed and approved
- **Archived**: Task removed from active workflow

### Priority Levels
- **Critical**: Must be done immediately, blocks other work
- **High**: Important, should be done soon
- **Medium**: Normal priority, scheduled work
- **Low**: Nice to have, can be deferred

### Technical Terms
- **Optimistic Update**: Update UI immediately, rollback if API fails
- **Debouncing**: Delay action until user stops typing (search, filters)
- **Infinite Scroll**: Load more items as user scrolls down
- **Real-time Sync**: WebSocket updates for live collaboration

---

## Verification Requirements

### Definition of Done
A task is considered complete when:
- [ ] All acceptance criteria met
- [ ] Code reviewed and approved
- [ ] Unit tests written and passing (min 80% coverage)
- [ ] Integration tests added for new APIs
- [ ] No TypeScript errors
- [ ] No ESLint warnings
- [ ] Passes all CI checks
- [ ] Manual testing completed
- [ ] Documentation updated
- [ ] Deployed to staging and verified

### Code Review Checklist
- [ ] Code follows project conventions
- [ ] No hardcoded values (use constants)
- [ ] Error handling implemented
- [ ] Loading states handled
- [ ] Edge cases considered
- [ ] Accessible (ARIA labels, keyboard navigation)
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] No console.log statements left in code
- [ ] Performance optimized (no unnecessary re-renders)

### Performance Benchmarks
- Initial page load: < 2 seconds
- Time to interactive: < 3 seconds
- API response time: < 500ms (p95)
- Lighthouse score: > 90
- Bundle size: < 200KB (gzipped)

---

## Common Gotchas & Known Issues

### Frequent Mistakes
1. **Forgetting to regenerate Prisma client** after schema changes
   - Fix: Run `npm run db:generate` after modifying `schema.prisma`

2. **Not handling loading/error states** in components
   - Always include loading spinners and error boundaries

3. **Mutating state directly** instead of using immutable updates
   - Use spread operators or Immer for state updates

4. **Not cleaning up useEffect hooks**
   - Return cleanup function for subscriptions, timers, listeners

5. **Circular dependencies** between modules
   - Restructure imports or use dependency injection

### Platform-Specific Issues
- **Windows**: Line endings (CRLF vs LF) - configure Git with `core.autocrlf=true`
- **macOS**: Case-sensitive imports - match exact file name casing
- **Linux**: File permissions - may need `chmod +x` for scripts

### Known Limitations
- File uploads limited to 10MB per file
- WebSocket connections limited to 100 per server instance
- Search queries limited to 100 characters
- Maximum 50 projects per workspace
- Real-time updates have ~1 second delay

### Debugging Tips
- Use React DevTools to inspect component state and props
- Use Redux DevTools for Zustand store debugging
- Check Network tab for API request/response details
- Enable verbose Prisma logging: `log: ['query', 'error', 'warn']`
- Use `console.trace()` to find where functions are called from

### Database Migration Issues
- If migration fails, run `npm run db:reset` (WARNING: destroys data)
- For production, create migration manually and test on staging first
- Never edit migration files after they've been applied

---

## Additional Resources

- **API Documentation**: `http://localhost:3000/api/docs` (Swagger)
- **Component Storybook**: Run `npm run storybook`
- **Architecture Diagrams**: See `/docs/architecture/`
- **Database Schema**: Open Prisma Studio with `npm run db:studio`

For questions or issues, contact the development team or create an issue in GitHub.
